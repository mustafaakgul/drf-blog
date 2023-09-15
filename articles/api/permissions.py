from rest_framework.permissions import BasePermission

class IsOwner(BasePermission): # Inherit from BasePermission
    message = "You must be the owner of this object."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    # bu metod isowner direk girince calısır ancak delete edncede has object calisir
    # yani delete url ornek alsn delete url girince has permission clisir delete bsnca
    # has objeect casliri
    # son halde browserdan delete vrunca authentike dglse calsmayacak dgerince ise
    # superuser veya kendsnnde sileblr has permssion girince drek clisir aksiyndada has objet dger metod clsr


    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user) or request.user.is_superuser
    # kullanıcı makale bnmse editlerm yada adminsem
    # is_staff bunu kysaydk staff ise grelbirdi
    # isadmin isstaff ise demektr method olara admn panele erisim ytkisi olan
