# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "sentinel automation-rule show",
)
class Show(AAZCommand):
    """Gets the automation rule
    """

    _aaz_info = {
        "version": "2021-10-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.operationalinsights/workspaces/{}/providers/microsoft.securityinsights/automationrules/{}", "2021-10-01"],
        ]
    }

    def _handler(self, command_args):
        super()._handler(command_args)
        self._execute_operations()
        return self._output()

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.automation_rule_id = AAZStrArg(
            options=["--automation-rule-id", "--name", "-n"],
            help="Automation rule ID",
            required=True,
            id_part="child_name_1",
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        _args_schema.workspace_name = AAZStrArg(
            options=["--workspace-name"],
            help="The name of the workspace.",
            required=True,
            id_part="name",
            fmt=AAZStrArgFormat(
                max_length=90,
                min_length=1,
            ),
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.AutomationRulesGet(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class AutomationRulesGet(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.OperationalInsights/workspaces/{workspaceName}/providers/Microsoft.SecurityInsights/automationRules/{automationRuleId}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "ODataV4Format"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "automationRuleId", self.ctx.args.automation_rule_id,
                    required=True,
                ),
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
                **self.serialize_url_param(
                    "workspaceName", self.ctx.args.workspace_name,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2021-10-01",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()

            _schema_on_200 = cls._schema_on_200
            _schema_on_200.etag = AAZStrType()
            _schema_on_200.id = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.properties = AAZObjectType(
                flags={"required": True, "client_flatten": True},
            )
            _schema_on_200.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _schema_on_200.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.properties
            properties.actions = AAZListType(
                flags={"required": True},
            )
            properties.created_by = AAZObjectType(
                serialized_name="createdBy",
                flags={"read_only": True},
            )
            _ShowHelper._build_schema_client_info_read(properties.created_by)
            properties.created_time_utc = AAZStrType(
                serialized_name="createdTimeUtc",
                flags={"read_only": True},
            )
            properties.display_name = AAZStrType(
                serialized_name="displayName",
                flags={"required": True},
            )
            properties.last_modified_by = AAZObjectType(
                serialized_name="lastModifiedBy",
                flags={"read_only": True},
            )
            _ShowHelper._build_schema_client_info_read(properties.last_modified_by)
            properties.last_modified_time_utc = AAZStrType(
                serialized_name="lastModifiedTimeUtc",
                flags={"read_only": True},
            )
            properties.order = AAZIntType(
                flags={"required": True},
            )
            properties.triggering_logic = AAZObjectType(
                serialized_name="triggeringLogic",
                flags={"required": True},
            )

            actions = cls._schema_on_200.properties.actions
            actions.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.actions.Element
            _element.action_type = AAZStrType(
                serialized_name="actionType",
                flags={"required": True},
            )
            _element.order = AAZIntType(
                flags={"required": True},
            )

            disc_modify_properties = cls._schema_on_200.properties.actions.Element.discriminate_by("action_type", "ModifyProperties")
            disc_modify_properties.action_configuration = AAZObjectType(
                serialized_name="actionConfiguration",
            )

            action_configuration = cls._schema_on_200.properties.actions.Element.discriminate_by("action_type", "ModifyProperties").action_configuration
            action_configuration.classification = AAZStrType()
            action_configuration.classification_comment = AAZStrType(
                serialized_name="classificationComment",
            )
            action_configuration.classification_reason = AAZStrType(
                serialized_name="classificationReason",
            )
            action_configuration.labels = AAZListType()
            action_configuration.owner = AAZObjectType()
            action_configuration.severity = AAZStrType()
            action_configuration.status = AAZStrType()

            labels = cls._schema_on_200.properties.actions.Element.discriminate_by("action_type", "ModifyProperties").action_configuration.labels
            labels.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.actions.Element.discriminate_by("action_type", "ModifyProperties").action_configuration.labels.Element
            _element.label_name = AAZStrType(
                serialized_name="labelName",
                flags={"required": True},
            )
            _element.label_type = AAZStrType(
                serialized_name="labelType",
                flags={"read_only": True},
            )

            owner = cls._schema_on_200.properties.actions.Element.discriminate_by("action_type", "ModifyProperties").action_configuration.owner
            owner.assigned_to = AAZStrType(
                serialized_name="assignedTo",
            )
            owner.email = AAZStrType()
            owner.object_id = AAZStrType(
                serialized_name="objectId",
            )
            owner.owner_type = AAZStrType(
                serialized_name="ownerType",
            )
            owner.user_principal_name = AAZStrType(
                serialized_name="userPrincipalName",
            )

            disc_run_playbook = cls._schema_on_200.properties.actions.Element.discriminate_by("action_type", "RunPlaybook")
            disc_run_playbook.action_configuration = AAZObjectType(
                serialized_name="actionConfiguration",
            )

            action_configuration = cls._schema_on_200.properties.actions.Element.discriminate_by("action_type", "RunPlaybook").action_configuration
            action_configuration.logic_app_resource_id = AAZStrType(
                serialized_name="logicAppResourceId",
                flags={"required": True},
            )
            action_configuration.tenant_id = AAZStrType(
                serialized_name="tenantId",
            )

            triggering_logic = cls._schema_on_200.properties.triggering_logic
            triggering_logic.conditions = AAZListType()
            triggering_logic.expiration_time_utc = AAZStrType(
                serialized_name="expirationTimeUtc",
            )
            triggering_logic.is_enabled = AAZBoolType(
                serialized_name="isEnabled",
                flags={"required": True},
            )
            triggering_logic.triggers_on = AAZStrType(
                serialized_name="triggersOn",
                flags={"required": True},
            )
            triggering_logic.triggers_when = AAZStrType(
                serialized_name="triggersWhen",
                flags={"required": True},
            )

            conditions = cls._schema_on_200.properties.triggering_logic.conditions
            conditions.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.triggering_logic.conditions.Element
            _element.condition_type = AAZStrType(
                serialized_name="conditionType",
                flags={"required": True},
            )

            disc_property = cls._schema_on_200.properties.triggering_logic.conditions.Element.discriminate_by("condition_type", "Property")
            disc_property.condition_properties = AAZObjectType(
                serialized_name="conditionProperties",
            )

            condition_properties = cls._schema_on_200.properties.triggering_logic.conditions.Element.discriminate_by("condition_type", "Property").condition_properties
            condition_properties.operator = AAZStrType()
            condition_properties.property_name = AAZStrType(
                serialized_name="propertyName",
            )
            condition_properties.property_values = AAZListType(
                serialized_name="propertyValues",
            )

            property_values = cls._schema_on_200.properties.triggering_logic.conditions.Element.discriminate_by("condition_type", "Property").condition_properties.property_values
            property_values.Element = AAZStrType()

            system_data = cls._schema_on_200.system_data
            system_data.created_at = AAZStrType(
                serialized_name="createdAt",
                flags={"read_only": True},
            )
            system_data.created_by = AAZStrType(
                serialized_name="createdBy",
                flags={"read_only": True},
            )
            system_data.created_by_type = AAZStrType(
                serialized_name="createdByType",
                flags={"read_only": True},
            )
            system_data.last_modified_at = AAZStrType(
                serialized_name="lastModifiedAt",
                flags={"read_only": True},
            )
            system_data.last_modified_by = AAZStrType(
                serialized_name="lastModifiedBy",
                flags={"read_only": True},
            )
            system_data.last_modified_by_type = AAZStrType(
                serialized_name="lastModifiedByType",
                flags={"read_only": True},
            )

            return cls._schema_on_200


class _ShowHelper:
    """Helper class for Show"""

    _schema_client_info_read = None

    @classmethod
    def _build_schema_client_info_read(cls, _schema):
        if cls._schema_client_info_read is not None:
            _schema.email = cls._schema_client_info_read.email
            _schema.name = cls._schema_client_info_read.name
            _schema.object_id = cls._schema_client_info_read.object_id
            _schema.user_principal_name = cls._schema_client_info_read.user_principal_name
            return

        cls._schema_client_info_read = _schema_client_info_read = AAZObjectType(
            flags={"read_only": True}
        )

        client_info_read = _schema_client_info_read
        client_info_read.email = AAZStrType(
            flags={"read_only": True},
        )
        client_info_read.name = AAZStrType(
            flags={"read_only": True},
        )
        client_info_read.object_id = AAZStrType(
            serialized_name="objectId",
            flags={"read_only": True},
        )
        client_info_read.user_principal_name = AAZStrType(
            serialized_name="userPrincipalName",
            flags={"read_only": True},
        )

        _schema.email = cls._schema_client_info_read.email
        _schema.name = cls._schema_client_info_read.name
        _schema.object_id = cls._schema_client_info_read.object_id
        _schema.user_principal_name = cls._schema_client_info_read.user_principal_name


__all__ = ["Show"]
