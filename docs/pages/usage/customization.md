---
layout: page
title: Customization
permalink: /pages/usage/customization/
weight: 104
---

## What are our solutions to achieve customized logic?
Normally, there are two ways to do customization:
- Inheritance: Inherit aaz commands and define customized logic in various callback actions. E.g.,
    ```python
    class AddressPoolCreate(_AddressPoolCreate):
        @classmethod
        def _build_arguments_schema(cls, *args, **kwargs):
            from azure.cli.core.aaz import AAZListArg, AAZStrArg

            args_schema = super()._build_arguments_schema(*args, **kwargs)
            args_schema.servers = AAZListArg(
                options=["--servers"],
                help="Space-separated list of IP addresses or DNS names corresponding to backend servers."
            )
            args_schema.servers.Element = AAZStrArg()
            args_schema.backend_addresses._registered = False

            return args_schema

        def pre_operations(self):
            args = self.ctx.args

            def server_trans(_, server):
                try:
                    socket.inet_aton(str(server))
                    return {"ip_address": server}
                except socket.error:
                    return {"fqdn": server}

            args.backend_addresses = assign_aaz_list_arg(
                args.backend_addresses,
                args.servers,
                element_transformer=server_trans
            )
    ```
    After that, please don't forget to add your customized command to our command table in _commands.py_:
    ```python
    def load_command_table(self, _):
        with self.command_group("network application-gateway address-pool"):
            from .custom import AddressPoolCreate, AddressPoolUpdate
            self.command_table["network application-gateway address-pool create"] = AddressPoolCreate(loader=self)
    ```
- Wrapper: Call aaz commands within previous implementation. E.g.,
    ```python
    def remove_ag_identity(cmd, resource_group_name, application_gateway_name, no_wait=False):
        class IdentityRemove(_ApplicationGatewayUpdate):
            def pre_operations(self):
                args = self.ctx.args
                args.no_wait = no_wait

            def pre_instance_update(self, instance):
                instance.identity = None

        return IdentityRemove(cli_ctx=cmd.cli_ctx)(command_args={
            "name": application_gateway_name,
            "resource_group": resource_group_name
        })
    ```
    After that, please don't forget to add your customized command to our command table in _commands.py_:
    ```python
    def load_command_table(self, _):
        with self.command_group("network application-gateway identity") as g:
            g.custom_command("remove", "remove_ag_identity", supports_no_wait=True)
    ```

We always prefer to the inheritance way, which is more elegant and easier to maintain. Unless you wanna reuse previous huge complicated logic or features that aaz-dev hasn't touched, we can consider the wrapper way (probably happens when migrating to aaz-dev).

For better understanding, you can firstly go through the above two examples. BTW, if there is no customization in your previous commands, aaz-dev is already naturally supported.

## How many callback actions are there in the codegen framework?
There are eight callback actions in total:
- For normal commands we have `pre_operations` and `post_operations`.
- For update commands we have two more callback actions: `pre_instance_update` and `post_instance_update`.
- For subcommands, there are four additional ones: `pre_instance_create`, `post_instance_create`, `pre_instance_delete` and `post_instance_delete`.

## How to add validation to your commands?
You can leverage our inheritance solution, i.e., inherit the generated class in _custom.py_ file and overwrite its `pre_operations` method:
```python
from .aaz.latest.network.application_gateway.url_path_map.rule import Create as _URLPathMapRuleCreate

class URLPathMapRuleCreate(_URLPathMapRuleCreate):
    def pre_operations(self):
        args = self.ctx.args
        if has_value(args.address_pool) and has_value(args.redirect_config):
            err_msg = "Cannot reference a BackendAddressPool when Redirect Configuration is specified."
            raise ArgumentUsageError(err_msg)
```

## How to clean up redundant properties?
Usually, we can remove useless properties in `post_instance_update`:
```python
def post_instance_update(self, instance):
    if not has_value(instance.properties.network_security_group.id):
        instance.properties.network_security_group = None
    if not has_value(instance.properties.route_table.id):
        instance.properties.route_table = None
```

## How to trim the output of a command?
As our code generation is written in Python, the output can be easily modified:
```python
from .aaz.latest.network.lb import Update

def foo():
    result = Update(cli_ctx=cmd.cli_ctx)(command_args={
        "name": load_balancer_name,
        "resource_group": resource_group_name,
        "probes": probes,
    }).result()["probes"]
    
    return [r for r in result if r["name"] == item_name][0]
```

## Can we add an extra output for a command?
If it is a simple operation, we can achieve that by rewriting `_output` method:
```python
def _output(self, *args, **kwargs):
    result = self.deserialize_output(self.ctx.selectors.subresource.required(), client_flatten=True)
    
    return result
```
If it is a long-running operation, we can do that:
```python
def _handler(self, command_args):
    lro_poller = super()._handler(command_args)
    lro_poller._result_callback = self._output

    return lro_poller

def _output(self, *args, **kwargs):
    result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
    
    return result
```

## How to support cross-subscription or cross-tenant?
It can be easily implemented by codegen framework, just declare the format of a parameter via template:
```python
@classmethod
def _build_arguments_schema(cls, *args, **kwargs):
    from azure.cli.core.aaz import AAZResourceIdArgFormat
    
    args_schema = super()._build_arguments_schema(*args, **kwargs)
    args_schema.frontend_ip._fmt = AAZResourceIdArgFormat(
        template="/subscriptions/{subscription}/resourceGroups/{resource_group}/providers/Microsoft.Network/applicationGateways/{gateway_name}/frontendIPConfigurations/{}"
    )

    return args_schema
```

## How to hide a command or a parameter to the users (only used for implementation)?
To hide a command, you can unregister a command in the CLI page; To hide a parameter:
```python
@classmethod
def _build_arguments_schema(cls, *args, **kwargs):
    args_schema.protocol._registered = False

    return args_schema
```

If the parameter is required, we need to firstly declare `_required` to be False:
```python
@classmethod
def _build_arguments_schema(cls, *args, **kwargs):
    args_schema.protocol._required = False
    args_schema.protocol._registered = False

    return args_schema
```

## How to achieve a long-running operation based on codegen?
It is similar as previous manual solution:
```python
from azure.cli.core.commands import LongRunningOperation

poller = VNetSubnetCreate(cli_ctx=self.cli_ctx)(command_args={
    "name": subnet_name,
    "vnet_name": metadata["name"],
    "resource_group": metadata["resource_group"],
    "address_prefix": args.subnet_prefix,
    "private_link_service_network_policies": "Disabled"
})

LongRunningOperation(self.cli_ctx)(poller)
```

## How to declare a file type argument?
It is nothing special, similar as others:
```python
@classmethod
def _build_arguments_schema(cls, *args, **kwargs):
    from azure.cli.core.aaz import AAZFileArg, AAZFileArgBase64EncodeFormat

    args_schema = super()._build_arguments_schema(*args, **kwargs)
    args_schema.cert_file = AAZFileArg(
        options=["--cert-file"],
        help="Path to the pfx certificate file.",
        fmt=AAZFileArgBase64EncodeFormat(),
        nullable=True,  # commonly used in update command
    )
    args_schema.data._registered = False

    return args_schema

def pre_operations(self):
    args = self.ctx.args
    if has_value(args.cert_file):
        args.data = args.cert_file
```

## How to show a secret property in the output?
The hidden of secret properties in output is by design, but we still support to show that:
```python
def _output(self, *args, **kwargs):
    result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True, secret_hidden=False)

    return result
```
