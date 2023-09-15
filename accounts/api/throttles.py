from rest_framework.throttling import AnonRateThrottle, SimpleRateThrottle, UserRateThrottle


class RegisterThrottle(SimpleRateThrottle):
    scope = 'registerthrottle'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated or request.method == "GET":
            return None  # Only throttle unauthenticated requests.

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


"""
class RegisterThrottle(AnonRateThrottle):

    scope = 'registerthrottle'
    #ana kullanrsan bu sklde grs ypmamıs kullanıcıda ip adresini al drek engeli bsyr
    #bu istek get veya post olablr

"""


# bunu postlist api postda kllncam
# bunda kullanıcı grisi yap dene engeli ye snra logout yap misafr oldn ordan tekrr greresen tekrr 6 kre istek atablrsn snra
# gene engellnr
class PostListUserThrottle(UserRateThrottle):
    scope = 'postlistuserthrottle'
    # ana kullanrsan bu sklde grs ypmamıs kullanıcıda ip adresini al drek engeli bsyr
    # bu istek get veya post olablr