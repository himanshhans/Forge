from rest_framework.throttling import ScopedRateThrottle


class GenerateThrottle(ScopedRateThrottle):
    scope = "generate"


class AvatarGenThrottle(ScopedRateThrottle):
    scope = "avatar_gen"


class DeployThrottle(ScopedRateThrottle):
    scope = "deploy"
