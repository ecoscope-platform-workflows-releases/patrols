# patrols
A workflow for generating a dashboard visualizing patrol trajectories, patrol events, and time density, from EarthRanger data.

## Recompiling

1. To recompile this workflow after having made changes to `spec.yaml`, first install `wt-compiler`
if you do not have it installed already:

    > **Note**: The `--run-post-link-scripts` flag is necessary because, in order to generate a visual
    representation of the workflow DAG, the `wt-compiler compile` command depends on the `dot` executable
    having been initialized post-install via the `dot -c` command. Setting the `--run-post-link-scripts`
    flag triggers this initialization automatically. Setting this flag does imply allowing the package
    manager to [run (potentially insecure) arbitrary scripts](https://pixi.prefix.dev/v0.62.2/reference/pixi_configuration/#run-post-link-scripts).
    If you prefer to omit this flag, then after you have installed `wt-compiler`, you may
    separately run `$HOME/.pixi/envs/wt-compiler/bin/dot -c` to initialize `dot`.

    ```console
    $ pixi global install \
    -c https://prefix.dev/ecoscope-workflows \
    -c conda-forge \
    wt-compiler \
    --run-post-link-scripts
    ```

2. Update pixi:

   > **Note**: We want to update pixi to the latest stable version locally before recompiling, because
   in the next step we will use the output of `pixi --version` to set the version of pixi used
   in the generated `Dockerfile`. Because pixi is a very fast-moving project, with performance
   improvements and bugfixes being released regularly, we want the version used here to be the
   latest stable version.

   ```console
   pixi self-update
   ```

3. Then from the repo root, run:

    > **Note**: Running `wt-compiler compile` will import all tasks from requirements defined
    in the `spec.yaml`'s `requirements:` section into an ephemeral environment on your machine.
    Please ensure that you trust the contents of these requirements before running the following
    command.

    ```console
    $ PIXI_VERSION="v$(pixi --version | awk '{print $2}')" \
    wt-compiler compile \
    --spec=spec.yaml \
    --pkg-name-prefix=ecoscope-workflows \
    --results-env-var=ECOSCOPE_WORKFLOWS_RESULTS \
    --variant=gcp \
    --update \
    --clobber

    ```

