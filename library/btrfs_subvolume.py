from ansible.module_utils.basic import AnsibleModule
import os.path
import os
import pwd
import grp


def check_btrfs_subvolume(module, path):
    rc, stdout, stderr = module.run_command(["stat", "-f", "--format", r"%T", path])
    if rc != 0:
        module.fail_json(
            msg=f"Failed to stat {path}",
            rc=rc,
            stdout=stdout,
            stderr=stderr,
        )

    if stdout.strip() != "btrfs":
        return False

    rc, stdout, stderr = module.run_command(["stat", "--format", r"%i", path])
    if rc != 0:
        module.fail_json(
            msg=f"Failed to stat {path}",
            rc=rc,
            stdout=stdout,
            stderr=stderr,
        )

    return int(stdout.strip()) == 256


def get_uid(user):
    try:
        uid = int(user)
        return uid
    except ValueError:
        return pwd.getpwnam(user).pw_uid


def get_gid(group):
    try:
        gid = int(group)
        return gid
    except ValueError:
        return grp.getgrnam(group).gr_gid


def remove_subvolume(module):
    path = module.params["path"]

    if not os.path.exists(path):
        module.exit_json(dict(changed=False))

    if not check_btrfs_subvolume(module, path):
        # path is not a btrfs subvolume
        # refusing to do anything
        module.fail_json(
            msg=f"{path} exists but is not a btrfs subvolume",
        )

    # remove subvolume
    if not module.check_mode:
        rc, stdout, stderr = module.run_command(["btrfs", "subvolume", "delete", path])
        if rc != 0:
            module.fail_json(
                msg=f"Failed to delete subvolume {path}",
                rc=rc,
                stdout=stdout,
                stderr=stderr,
            )

    # subvolume has successfully been removed
    module.exit_json(dict(changed=True))


def create_subvolume(module):
    path = module.params["path"]
    result = dict(changed=False)

    # create missing submodule
    if not os.path.exists(path):
        if not module.check_mode:
            rc, stdout, stderr = module.run_command(
                ["btrfs", "subvolume", "create", path]
            )
            if rc != 0:
                module.fail_json(
                    msg=f"Failed to create subvolume {path}",
                    rc=rc,
                    stdout=stdout,
                    stderr=stderr,
                )
        result["changed"] = True
    else:
        # something exists at path
        if not check_btrfs_subvolume(module, path):
            # but it is not a btrfs subvolume, refusing to do anything
            module.fail_json(
                msg=f"{path} exists but is not a btrfs subvolume",
            )

    current_uid = os.stat(path).st_uid
    current_gid = os.stat(path).st_gid
    owner = module.params["owner"]
    group = module.params["group"]
    uid = get_uid(owner) if owner else current_uid
    gid = get_gid(group) if group else current_gid

    if (uid != current_uid) or (gid != current_gid):
        result["changed"] = True
        if not module.check_mode:
            rc, stdout, stderr = module.run_command(
                [
                    "chown",
                    f"{uid}:{gid}",
                    path,
                ]
            )
            if rc != 0:
                module.fail_json(
                    msg=f"Failed to chown {path}",
                    rc=rc,
                    stdout=stdout,
                    stderr=stderr,
                )

    module.exit_json(**result)


def run_module():
    module_args = dict(
        path=dict(
            type="path",
            required=True,
        ),
        state=dict(
            default="present",
            choices=[
                "present",
                "absent",
            ],
        ),
        owner=dict(
            type="str",
            required=False,
        ),
        group=dict(
            type="str",
            required=False,
        ),
    )
    result = dict(
        changed=False,
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    state = module.params["state"]
    if state == "absent":
        remove_subvolume(module)
    elif state == "present":
        create_subvolume(module)


def main():
    run_module()


if __name__ == "__main__":
    main()
