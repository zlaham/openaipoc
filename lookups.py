from enum import Enum
import pandas as pd

class FunctionReturn(Enum):
    SUCCESS = "success"
    FAIL = "fail"

class DataTypes(Enum):
    FLOAT = "<class 'float'>"
    STR = "<class 'str'>"
    DATETIME = "<class 'datetime.date'>"
    INT = "<class 'str'>"
    BOOL = "<class 'bool'>"
    TIMESTAMP = "<class 'pandas._libs.tslibs.timestamps.Timestamp'>"


class TableType(Enum):
    STAGING = "staging"
    DIMENSION = "dimension"
    FACT = "fact"
    AGGREGATE = "aggregate"
    VIEWS = "views"


translation_configurations = pd.Series(data=["stg_building_take_down_dept","stg_building_take_down_job","stg_building_take_down_result","stg_rent_contract_reg_dept","stg_rent_contract_reg_job","stg_rent_contract_registration_result"], index=["department_name","job_name","result_desc","department_name","job_name","result_desc"])


