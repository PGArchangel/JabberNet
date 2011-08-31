/*
    Copyright (C) 2011 Dotsenko A.N. Link <pgandrey@yandex.ru>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2 as
    published by the Free Software Foundation.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    Please tell me, if you find errors or mistakes.

Based on parts of the GNU C Library:

   Common code for file-based database parsers in nss_files module.
   Copyright (C) 1996, 1997, 1998, 1999, 2000 Free Software Foundation, Inc.
   This file is part of the GNU C Library.

   The GNU C Library is free software; you can redistribute it and/or
   modify it under the terms of the GNU Lesser General Public
   License as published by the Free Software Foundation; either
   version 2.1 of the License, or (at your option) any later version.

   The GNU C Library is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Lesser General Public License for more details.
*/

#define _GNU_SOURCE 1

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <nss.h>
#include <pwd.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
#include <errno.h>
#include <ctype.h>
#include <string.h>

#include "s_config.h"
#include "daemon.h"

enum nss_status _nss_jabbernet_getpwuid_r(uid_t,struct passwd *,char *, size_t,int *);
enum nss_status _nss_jabbernet_setpwent (void);
enum nss_status _nss_jabbernet_endpwent (void);
enum nss_status _nss_jabbernet_getpwnam_r(const char *,struct passwd *,char *,size_t,int *);
enum nss_status _nss_jabbernet_getpwent_r(struct passwd *, char *, size_t,int *);

static int sock=0;

enum nss_status _nss_jabbernet_getpwuid_r( uid_t uid, struct passwd *result,
	char *buf, size_t buflen, int *errnop)
{
//	printf("Executed function: '_nss_jabbernet_getpwuid_r'...");
	*errnop = 0;
	if ( result!=NULL )
	{
		int sock=jabbernet_connectTo(AF_INET);
		if (sock==-1) {return NSS_STATUS_UNAVAIL;}
		enum nss_status n = jabbernet_getUser(sock,NULL,uid,result,errnop,buf,buflen);
		jabbernet_close(sock);
		return n;
	}
	else
	{
		return NSS_STATUS_UNAVAIL;
	}
}

enum nss_status _nss_jabbernet_getpwnam_r(const char *name, struct passwd *result,
		char *buf, size_t buflen, int *errnop)
{
//	printf( "Executed function: '_nss_jabbernet_getpwnam_r'...");
	*errnop = 0;
	if ( result )
	{
		int sock=jabbernet_connectTo(AF_INET);
		if (sock==-1) {return NSS_STATUS_UNAVAIL;}
		enum nss_status n = jabbernet_getUser(sock,name,0,result,errnop,buf,buflen);
		jabbernet_close(sock);
		return n;
	}
	else
		return NSS_STATUS_UNAVAIL;
}

enum nss_status _nss_jabbernet_setpwent (void)
{
//	printf("Executed function: '_nss_jabbernet_setpwent'...");
	sock=jabbernet_connectTo(AF_INET);
	if (sock==-1) {return NSS_STATUS_UNAVAIL;}
	return jabbernet_toFirstUser(sock);
//	return NSS_STATUS_SUCCESS;
}

enum nss_status _nss_jabbernet_endpwent (void)
{
//	printf("Executed function: '_nss_jabbernet_endpwent'...");
	jabbernet_close(sock);
	return NSS_STATUS_SUCCESS;
}

enum nss_status _nss_jabbernet_getpwent_r (struct passwd *pw,
                char * buffer, size_t buflen,int * errnop)
{
//	printf("Executed function: '_nss_jabbernet_getpwent_r'...");
	*errnop = -1;

	if ( pw == NULL )
		return NSS_STATUS_UNAVAIL;

	if (sock>0)
	{
		enum nss_status n = jabbernet_getUser(sock,NULL,0,pw,errnop,buffer,buflen);
		return n;
	} else {return NSS_STATUS_UNAVAIL;}
}

