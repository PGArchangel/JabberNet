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
#define _FILE_OFFSET_BITS 64

#include <stdio.h>
#include <stdlib.h>
#include <nss.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
#include <errno.h>
#include <ctype.h>
#include <grp.h>

#include "s_config.h"
#include "daemon.h"

enum nss_status _nss_jabbernet_setgrent (void); // Перемещает указатель на начало списка групп
enum nss_status _nss_jabbernet_endgrent (void); // Закрывает список
enum nss_status _nss_jabbernet_getgrent_r (struct group *gr,
		char * buffer, size_t buflen,int * errnop); // 
enum nss_status _nss_jabbernet_getgrnam_r (const char * name, struct group *gr,
		char * buffer, size_t buflen,int *errnop);
enum nss_status _nss_jabbernet_getgrgid_r (const gid_t gid, struct group *gr,
		char * buffer, size_t buflen,int *errnop);



int sock=0;

enum nss_status _nss_jabbernet_setgrent (void) {
	sock=jabbernet_connectTo(AF_INET);
	if( sock<=0 )
		return NSS_STATUS_UNAVAIL;
	return jabbernet_toFirstGroup(sock);
}

enum nss_status _nss_jabbernet_endgrent (void) {
	jabbernet_close(sock);
	return NSS_STATUS_SUCCESS;
}

enum nss_status _nss_jabbernet_getgrent_r (struct group *gr,
		char * buffer, size_t buflen,int * errnop)
{
	*errnop = 0;
	if (sock==-1) {return NSS_STATUS_UNAVAIL;}
	enum nss_status e = jabbernet_getGroup(sock,NULL,0,gr,errnop,buffer,buflen);
	return e;
}


enum nss_status _nss_jabbernet_getgrnam_r (const char * name, struct group *gr,
		char * buffer, size_t buflen,int *errnop)
{
	enum nss_status e;

	*errnop = 0;
	
//	printf("Buffer length: %d\n",buflen);

	if ( gr == NULL || name == NULL )
		return NSS_STATUS_UNAVAIL;

	int sock=jabbernet_connectTo(AF_INET);
	if (sock==-1) {return NSS_STATUS_UNAVAIL;}
	e = jabbernet_getGroup(sock,name,0,gr,errnop,buffer,buflen);

	jabbernet_close(sock);

	return e;
}

enum nss_status _nss_jabbernet_getgrgid_r (const gid_t gid, struct group *gr,
		char * buffer, size_t buflen,int *errnop)
{
	enum nss_status e;
	FILE *f;
	*errnop = 0;
	if ( gr == NULL )
		return NSS_STATUS_UNAVAIL;
	if( gid <= 0 )
		return NSS_STATUS_NOTFOUND;

	int sock=jabbernet_connectTo(AF_INET);
	if (sock==-1) {return NSS_STATUS_UNAVAIL;}
	e = jabbernet_getGroup(sock,NULL,gid,gr,errnop,buffer,buflen);
	jabbernet_close(sock);

	return e;
}
