#include <sys/socket.h>

int jabbernet_connectTo(sa_family_t family);


enum nss_status jabbernet_getUser(int sock, char* name, const uid_t uid, struct passwd *pw, int *errnop,char *buffer, size_t buflen);
enum nss_status jabbernet_getGroup(int sock,const char *name,const gid_t gid,struct group * gr, int * errnop,char * buffer, size_t buflen);
enum nss_status jabbernet_getShadow (int sock, const char *name, struct spwd *spw, int * errnop, char *buffer, size_t buflen);
