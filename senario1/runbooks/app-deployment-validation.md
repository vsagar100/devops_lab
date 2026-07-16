0. set current namespace to cloudops for ease of use
   kubectl config set-context --current --namespace=cloudops
1. Check rollout status
    $kubectl rollout status deployment/checkout-api -n cloudops
2. Check pods
    $kubectl get pods -o wide
3. Check service endpoint
    $kubectl get svc 
    $kubectl get endpoints checkout-api-svc -o wide
4. Test service from inside pod
   $kubectl run -rm curl-test -it --image=curl -- curl http://checkout-api.svc/health
5. Test ingress from jumpbox
    ## As we have configured service type "ClusterIP" we won't be able to test it outside K8s network.
6. Check logs
    $kubectl logs -l app=checkout-api --tail=100
7. Rollback command
    k rollout undo deployment/checkout-api
