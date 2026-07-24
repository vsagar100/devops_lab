## Pipeline 2 — Kubernetes Manifest Quality Gate Pipeline

### Purpose: Before any Kubernetes YAML is merged, validate it like a production platform team.
    This pipeline should run on PR when files under k8s/ change.

    Expected checks:

        1. YAML syntax validation
        2. kubeconform / kubeval schema validation
        3. kubectl dry-run validation
        4. kube-linter or kube-score
        5. checkov or conftest policy checks
        6. block risky configs

    Example risky configs to catch:

        container running as root
        missing resource requests/limits
        missing probes
        latest image tag
        privileged container
        hostPath volume
        Service type LoadBalancer/NodePort without approval
        NetworkPolicy missing
        HPA status field committed
        Secret values committed in plain text
