import json

from pydantic import BaseModel, ConfigDict

from src.utils.dicts import del_dict_key_recursively, del_dict_key_recursively_v2, camel_to_snake


class BaseSchemaModel(BaseModel):
    # func_name: str = "unknown"
    # func_description: str = "unknown"

    model_config = ConfigDict(extra="ignore")

    @classmethod
    def example(cls) -> dict:
        raise NotImplementedError()

    def purify(self):
        """自我净化"""
        pass

    @classmethod
    def schema(cls, without_title: bool = True, required: bool = False, **kwargs) -> dict:
        raw_schema: dict = super().model_json_schema(**kwargs)
        if without_title:
            del_dict_key_recursively(raw_schema, "title")
        # ! 删除所有 model_config, 这是一个 pydantic 配置字段
        del_dict_key_recursively(raw_schema, "model_config")

        # ! 删除所有 object 的 一级 description , 这通常是来自 docstrings
        del_dict_key_recursively_v2(
            raw_schema,
            get_del_keys_func=lambda d: ["description"]
            if d.get("type", None) == "object" and "description" in d
            else [],
        )
        if not required:
            raw_schema['required'] = []
        return {"type": "function",
                "function": {
                    "name": f"get_{camel_to_snake(cls.__name__.strip())}",
                    "description": cls.__doc__.strip() if cls.__doc__ else "unknown",
                    "parameters": raw_schema,
                }
                }

    def dict(
            self, include=None, exclude=None, by_alias: bool = False, **kwargs
    ) -> dict:
        if exclude is None:
            exclude = {}
        raw_dict: dict = super().dict(
            include=include,
            exclude={"model_config", *exclude},
            by_alias=by_alias,
            **kwargs,
        )
        return raw_dict

    @classmethod
    def schema_json(cls, without_title: bool = True, **kwargs) -> str:
        schema_dict: dict = cls.schema(without_title, **kwargs)
        return json.dumps(schema_dict, ensure_ascii=False)

