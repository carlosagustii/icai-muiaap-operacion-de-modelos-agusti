from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo #añado ValidationInfo para el field valid


# TODO: clase PrestamoEntrada (BaseModel) con las 6 variables del modelo, con sus rangos (ver enunciado).
#       Debe rechazar campos que no existan.
class PrestamoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid") 

    edad: int = Field(ge= 18, le=75)
    ingresos_mensuales: float = Field(gt=0)
    importe_prestamo: float = Field(gt=0) 
    plazo_meses: int = Field(ge=6, le=84)
    antiguedad_laboral_anios: int = Field(ge=0, le=50)
    impagos_previos: int = Field(ge=0, le=20)

    # TODO: field_validator (con classmethod) para antiguedad_laboral_anios: no puede ser incoherente con la edad.
    @field_validator('antiguedad_laboral_anios') #se mete el valor que validas, value abajo
    @classmethod
    def coherencia_antiguedad(cls, value, info: ValidationInfo):
        edad = info.data.get("edad") #info contiene un diccionario o algo que accedes a todos los valores ya validados
        if edad is not None:
            if value > (edad -16):
                raise ValueError("Tiene mas años trabajando que los que puede haber hecho fisicamente")
        return value 
    
# TODO: clase PrediccionSalida con probabilidad_impago (entre 0 y 1) y decision (aprobar, revisar o rechazar).
class PrediccionSalida(BaseModel):
    probabilidad_impago: float = Field(ge=0,le=1)
    decision: Literal["aprobar", "revisar", "rechazar"] 
