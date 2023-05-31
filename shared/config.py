import os
from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=[
        "devops/dynaconf/settings.toml",
        "devops/dynaconf/secrets.toml",
    ],  # Paths to globs or any toml|yaml|ini|json|py
    environments=True,  # Enable layered environments (Testind, DEV, SIT, PROD)
    load_dotenv=True,  # Loads envars from a .env file
    envar_prefix=False,  # variables exoirted as `DYNACONF_FOO=bar` becomes `settings.FOO=bar`
    env_switcher="ENV_FOR_DYNACONF",  # Exported variable to use for environment switch
    dotenv_path="devops/dynaconf/.env",  # Path to the envirnoments file
)


def get_envar(name: str):
    """
    Gets envar from dynaonf and if not avaliable, from os.environ.
    Raises RuntimeError if the variable is not avaliable in any of these.
    """
    value = settings.get(name, os.environ.get(name))
    if not value:
        raise RuntimeError(
            f"{name} could not be found in dynaconf settings nor as envar"
        )
    return value


if __name__ == "__main__":
    # Used only as validation when running as a script

    assert settings.env_for_dynaconf

    print("All assertions passed.")
