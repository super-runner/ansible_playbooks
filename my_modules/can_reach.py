#!/usr/bin/python


DOCUMENTATION = '''
---
module: can_reach
short_description: Checks server reachability
description:
 - Checks if a remote server can be reached
version_added: "1.8"
options:
  host:
    description:
      - A DNS hostname or IP address
    required: true
  port:
    description:
    - The TCP port number
    required: true
  timeout:
    description:
    - The amount of time trying to connect before giving up, in seconds
    required: false
    default: 3
  flavor:
    description:
    - This is a made-up option to show how to specify choices.
    required: false
    choices: ["chocolate", "vanilla", "strawberry"]
    aliases: ["flavor"]
    default: chocolate
requirements: [netcat]
author: Lorin Hochstein
notes:
  - This is just an example to demonstrate how to write a module.
  - You probably want to use the native M(wait_for) module instead.
'''

EXAMPLES = '''
# Check that ssh is running, with the default timeout
- can_reach: host=myhost.example.com port=22

# Check if postgres is running, with a timeout
- can_reach: host=db.example.com port=5432 timeout=1
'''

from ansible.module_utils.basic import AnsibleModule

def can_reach(module, host, port, timeout):
    nc_path = module.get_bin_path('nc', required=True)
    args = [nc_path, "-z", "-w", str(timeout), host, str(port)]
    (rc, stdout, stderr) = module.run_command(args)
    return rc == 0

def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True),
            port=dict(required=True, type='int'),
            timeout=dict(required=False, type='int', default=3)
        ),
        supports_check_mode=True
    )

    # In check mode, we take no action
    # Since this module never changes system state, we just
    # return changed=False
    if module.check_mode:
        module.exit_json(changed=False)

    host = module.params['host']
    port = module.params['port']
    timeout = module.params['timeout']

    if can_reach(module, host, port, timeout):
        module.exit_json(changed=False)
    else:
        msg = "Could not reach %s:%s" % (host, port)
        module.fail_json(msg=msg)

if __name__ == "__main__":
    main()
