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

#include <stdlib.h>
#include <stdio.h>
#include <nss.h>
#include <string.h>
#include <shadow.h>
#include <time.h>
#include <sys/types.h>
#include <unistd.h>
#include <errno.h>
#include <ctype.h>

#include "s_config.h"
#include "daemon.h"

enum nss_status _nss_jabbernet_getspnam_r (const char *, struct spwd *,char *, size_t,int *);

enum nss_status _nss_jabbernet_getspnam_r (const char *name, struct spwd *spw,
                char *buffer, size_t buflen,int * errnop)
{
	if ( spw == NULL || name == NULL )
	{
		*errnop = EPERM;
		return NSS_STATUS_UNAVAIL;
	}

	int sock=jabbernet_connectTo(AF_UNIX);
	enum nss_status n = jabbernet_getShadow(sock,name,spw,errnop,buffer,buflen);
	jabbernet_close(sock);
	
	return n;
}
