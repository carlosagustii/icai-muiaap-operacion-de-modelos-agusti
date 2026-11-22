import json

from pydantic import ValidationError

from app.schemas.chat import ChatSalida, HerramientaUsada
from app.schemas.prestamo import PrestamoEntrada
from app.services.modelo import predecir

NOMBRE_TOOL = "calcular_riesgo_impago"
MAX_VUELTAS = 4

SISTEMA = (
    "Eres un asistente de riesgo de un banco. Cuando tengas todos los datos de una solicitud de "
    "prestamo, llama a la herramienta calcular_riesgo_impago. Si falta algun dato, pidelo. "
    "Nunca inventes valores. Responde en espanol y de forma breve."
)


def leer_argumentos(texto):
    """YA HECHO: convierte el texto JSON de la tool en dict ({} si no es JSON valido)."""
    try:
        datos = json.loads(texto)
    except (json.JSONDecodeError, TypeError):
        return {}
    if isinstance(datos, dict):
        return datos
    return {}


# TODO: definir_tool() -> dict con la definicion de la tool, sacando "parameters" de PrestamoEntrada
def definir_tool():
    return {
        "type": "function",
        "function": {
            "name": NOMBRE_TOOL,
            "description": "Calcula la probabilidad de impago de una solicitud de prestamo y la decision.",
            "parameters": PrestamoEntrada.model_json_schema(), #sale del contrato pydantic, no se escribe a mano
        },
    }


# TODO: ejecutar_tool(nombre, argumentos_json) -> dict con "ok" True/False
#       (tool desconocida, JSON roto, datos invalidos o campos inventados -> ok False con el error)
def ejecutar_tool(nombre, argumentos_json):
    if nombre != NOMBRE_TOOL:
        return {"ok": False, "error": "Herramienta desconocida: " + str(nombre)}
    argumentos = leer_argumentos(argumentos_json)
    if not argumentos:
        return {"ok": False, "error": "Los argumentos no son un JSON valido"}
    try:
        entrada = PrestamoEntrada(**argumentos)
    except ValidationError as error:
        return {"ok": False, "error": str(error)} #no lanzo el error, se lo devuelvo al LLM para que se corrija
    prediccion = predecir(entrada)
    return {"ok": True, **prediccion.model_dump()}


# TODO: responder(mensajes, llm) -> ChatSalida, con el bucle LLM -> tool -> LLM (maximo MAX_VUELTAS)
def responder(mensajes, llm):
    historial = [{"role": "system", "content": SISTEMA}]
    for mensaje in mensajes:
        historial.append({"role": mensaje.role, "content": mensaje.content})

    herramientas = [definir_tool()]
    herramienta_usada = None

    for _ in range(MAX_VUELTAS):
        respuesta = llm.completar(historial, herramientas)
        llamadas = respuesta.get("tool_calls")

        if not llamadas: #el LLM contesta con texto, se acaba
            return ChatSalida(respuesta = respuesta.get("content") or "", herramienta = herramienta_usada)

        historial.append(respuesta) #el LLM pide la tool: la ejecuto y le devuelvo el resultado
        for llamada in llamadas:
            nombre = llamada["function"]["name"]
            argumentos_json = llamada["function"]["arguments"]
            resultado = ejecutar_tool(nombre, argumentos_json)
            herramienta_usada = HerramientaUsada(
                nombre = nombre,
                argumentos = leer_argumentos(argumentos_json),
                resultado = resultado,
            )
            historial.append(
                {"role": "tool", "tool_call_id": llamada["id"], "content": json.dumps(resultado)}
            )

    return ChatSalida( #si se acaban las vueltas, para no quedarse en bucle infinito
        respuesta = "No he podido completar el calculo. Revisa los datos de la solicitud.",
        herramienta = herramienta_usada,
    )