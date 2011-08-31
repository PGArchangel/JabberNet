/*
    Copyright (C) 2001,2002,2009 Bernhard R. Link <brlink@debian.org>

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

#include <stdio.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <netinet/in.h>
#include <nss.h>
#include <pwd.h>
#include <grp.h>
#include <shadow.h>
#include <errno.h>

#include <string.h>


#include "daemon.h"


/* from clib/nss */
static inline char **parse_list(char *line,char *data,size_t datalen,int *errnop) {
	char *eol, **list, **p;

	if (line >= data && line < (char *) data + datalen)
		/* Find the end of the line buffer, we will use the space in DATA after
		 *        it for storing the vector of pointers.  */
		eol = strchr (line, '\0') + 1;
	else
		/* LINE does not point within DATA->linebuffer, so that space is
		 *        not being used for scratch space right now.  We can use all of
		 *               it for the pointer vector storage.  */
		eol = data;
	/* Adjust the pointer so it is aligned for storing pointers.  */
	eol += __alignof__ (char *) - 1;
	eol -= (eol - (char *) 0) % __alignof__ (char *);
	/* We will start the storage here for the vector of pointers.  */
	list = (char **) eol;

	p = list;
	while (1)
	{
		char *elt;

		if ((size_t) ((char *) &p[1] - (char *) data) > datalen)
		{
			/* We cannot fit another pointer in the buffer.  */
			*errnop = ERANGE;
			return NULL;
		}
		if (*line == '\0')
			break;

		/* Skip leading white space.  This might not be portable but useful.  */
		while (isspace (*line))
			++line;

		elt = line;
		while (1) {
			if (*line == '\0' || *line == ',' ) {
				/* End of the next entry.  */
				if (line > elt)
					/* We really found some data.  */
					*p++ = elt;

				/* Terminate string if necessary.  */
				if (*line != '\0')
					*line++ = '\0';
				break;
			}
			++line;
		}
	}
	*p = NULL;

	return list;
}


int jabbernet_connectTo(sa_family_t family)
{
    int sock; // дескриптор сокета
    struct sockaddr *remote;
    int len;
    if (family==AF_INET)
    {
        struct sockaddr_in remote_in;
        remote_in.sin_family = family;
        remote_in.sin_port=htons(2477);
        inet_aton("127.0.0.1", &remote_in.sin_addr.s_addr);
        len=sizeof(remote_in);
        remote=(struct sockaddr *)&remote_in;
    }
    else if (family==AF_UNIX)
    {
        struct sockaddr_un remote_un;
        remote_un.sun_family = family;
        char* str="/home/arch/jabber bots/JabberNet/bot_client.sock";
        strcpy(remote_un.sun_path, str);
        len = strlen(remote_un.sun_path) + sizeof(remote_un.sun_family);
        remote=(struct sockaddr *)&remote_un;
    }


    if ((sock=socket(family, SOCK_STREAM, 0))==-1)
    {
        perror("socket");
        return -1;
    }

//    if (connect(sock, (struct sockaddr *)&remote, len) == -1) {
    if (connect(sock, remote, len) == -1) {
        perror("connect");
        return -1;
    }

 //   printf("Connected.\n");
    return sock;
}

int jabbernet_close(int sock)
{
    int n;
    char* sbuf="exit\r";
    n = write(sock,sbuf,strlen(sbuf));
    close(sock);
}

enum nss_status jabbernet_toFirstUser(int sock)
{
    char sbuf[1024];
    int n; // количество считанных байт


    char* s="%nss toFirstUser";
    n = write(sock,s,strlen(s));

    bzero(sbuf,1024);
    n = read(sock,sbuf,1024);
    if (sbuf[0]=='1')
    {
        return NSS_STATUS_SUCCESS;
    }
    else
    {
        return NSS_STATUS_UNAVAIL;
    }


}

enum nss_status jabbernet_toFirstGroup(int sock)
{
    char sbuf[1024];
    int n; // количество считанных байт


    char* s="%nss toFirstGroup";
    n = write(sock,s,strlen(s));

    bzero(sbuf,1024);
    n = read(sock,sbuf,1024);
    if (sbuf[0]=='1')
    {
        return NSS_STATUS_SUCCESS;
    }
    else
    {
        return NSS_STATUS_UNAVAIL;
    }


}

enum nss_status jabbernet_getUser(int sock, char* name, const uid_t uid, struct passwd *pw, int *errnop,char *buffer, size_t buflen)
{
    if ( pw == NULL )
	{
		*errnop = EPERM;
		return NSS_STATUS_UNAVAIL;
	}
    char sbuf[1024];
    int n; // количество считанных байт


    bzero(sbuf,1024);
//    char* s=sprintf("\%nss getUser %s\r",name);
    char* s;
    s=malloc(256);

//    char* t="%%nss getUser%s";
    char* t_a;
    char* t_l;
    t_l=malloc(256);
    t_a=malloc(256);
    bzero(t_l,256);
    bzero(t_a,256);
//    if (name==NULL) {printf("Name is not defined...");}
//    else {printf("%s\n",name);}
    if (name!=NULL) {sprintf(t_l," pw_name=%s",name);t_a=strcat(t_a,t_l);}
    if (uid>0) {sprintf(t_l," pw_uid=%d",uid);t_a=strcat(t_a,t_l);}

    sprintf(s,"%%nss getUser%s",t_a);


    strcpy((char*)&sbuf,s);
    free(t_a);
    free(t_l);
    free(s);

//    printf("Sending query: %s\n",sbuf);
    n = write(sock,sbuf,strlen(sbuf));
    if (n < 0)
        perror("write");
    bzero(sbuf,1024);
    n = read(sock,sbuf,1024);



    strcpy(buffer,(char*)&sbuf);

    s = strtok (buffer,"\n");
//    printf("Result: %s\n",s);
    n=strcmp(s,"1");
//    printf("Comparing result: %d\n",n);
    if (n==0)
    {
 //       printf("User found...\n");
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {pw->pw_name=s;} else {pw->pw_name=NULL;}
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {pw->pw_uid = atoi(s);} else {pw->pw_uid =0;}
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {pw->pw_passwd = s;} else {pw->pw_passwd = s;}
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {pw->pw_gid = atoi(s);} else {pw->pw_gid = 0;}
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {pw->pw_gecos = s;} else {pw->pw_gecos = NULL;}
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {pw->pw_dir = s;} else {pw->pw_dir = s;}
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {pw->pw_shell = s;} else {pw->pw_shell = s;}
    //    printf(s);

        *errnop = 0;

        return NSS_STATUS_SUCCESS;
    }
    else
    {
        *errnop = ENOENT;
 //       printf("User not found...\n");
        return NSS_STATUS_NOTFOUND;
    }
}


enum nss_status jabbernet_getGroup(int sock,const char *name,const gid_t gid,struct group * gr, int * errnop,char * buffer, size_t buflen)
{
    if ( gr == NULL )
	{
		*errnop = EPERM;
		return NSS_STATUS_UNAVAIL;
	}
    char sbuf[1024];
    int n; // количество считанных байт


    bzero(sbuf,1024);
//    char* s=sprintf("\%nss getUser %s\r",name);
    char* s;
    s=malloc(256);

//    char* t="%%nss getUser%s";
    char* t_a;
    char* t_l;
    t_l=malloc(256);
    t_a=malloc(256);
    bzero(t_l,256);
    bzero(t_a,256);
//    if (name==NULL) {printf("Name is not defined...");}
//    else {printf("%s\n",name);}
    if (name!=NULL) {sprintf(t_l," gr_name=%s",name);t_a=strcat(t_a,t_l);}
    if (gid>0) {sprintf(t_l," gr_gid=%d",gid);t_a=strcat(t_a,t_l);}

    sprintf(s,"%%nss getGroup%s",t_a);


    strcpy((char*)&sbuf,s);
    free(t_a);
    free(t_l);
    free(s);

 //   printf("Sending query: %s\n",sbuf);
    n = write(sock,sbuf,strlen(sbuf));
    if (n < 0)
        perror("write");
    bzero(sbuf,1024);
    n = read(sock,sbuf,1024);



    strcpy(buffer,(char*)&sbuf);

    s = strtok (buffer,"\n");
 //   printf("Result: %s\n",s);
    n=strcmp(s,"1");
//    printf("Comparing result: %d\n",n);

    char *ss;

    if (n==0)
    {
 //       printf("User found...\n");


        s = strtok (NULL,"\n");
        if (s!=NULL) {gr->gr_name=s;} else {gr->gr_name=NULL;}
//        printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {gr->gr_passwd = s;} else {gr->gr_passwd=NULL;}
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {gr->gr_gid = atoi(s);} else {gr->gr_gid=0;}
        if (s!=NULL) {ss=s;} else {ss=ss+sizeof(gr->gr_gid);}
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {gr->gr_mem = parse_list(s,buffer,buflen,errnop);} else {gr->gr_mem =parse_list(ss+sizeof(gr->gr_gid),buffer,buflen,errnop);;}
    //    printf(s);

         *errnop = 0;


        return NSS_STATUS_SUCCESS;
    }
    else
    {
        *errnop = ENOENT;
 //       printf("User not found...\n");
        return NSS_STATUS_NOTFOUND;
    }
}


enum nss_status jabbernet_getShadow (int sock, const char *name, struct spwd *spw, int * errnop, char *buffer, size_t buflen)
{

    char sbuf[1024];
    int n; // количество считанных байт


    bzero(sbuf,1024);
//    char* s=sprintf("\%nss getUser %s\r",name);
    char* s;
    s=malloc(256);

//    char* t="%%nss getUser%s";
    char* t_a;
    char* t_l;
    t_l=malloc(256);
    t_a=malloc(256);
    bzero(t_l,256);
    bzero(t_a,256);
//    if (name==NULL) {printf("Name is not defined...");}
//    else {printf("%s\n",name);}
    if (name!=NULL) {sprintf(t_l," sp_namp=%s",name);t_a=strcat(t_a,t_l);}

    sprintf(s,"%%nss getShadow%s",t_a);


    strcpy((char*)&sbuf,s);
    free(t_a);
    free(t_l);
    free(s);

//    printf("Sending query: %s\n",sbuf);
    n = write(sock,sbuf,strlen(sbuf));
    if (n < 0)
        perror("write");
    bzero(sbuf,1024);
    n = read(sock,sbuf,1024);



    strcpy(buffer,(char*)&sbuf);

    s = strtok (buffer,"\n");
//    printf("Result: %s\n",s);
    n=strcmp(s,"1");
//    printf("Comparing result: %d\n",n);

    if (n==0)
    {
//        printf("User found...\n");
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {spw->sp_namp=s;} else {spw->sp_namp=NULL;}
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {spw->sp_pwdp = s;} else {spw->sp_pwdp = NULL;}
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {spw->sp_lstchg = atoi(s);} else {spw->sp_lstchg = 0;}
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {spw->sp_min = atoi(s);} else {spw->sp_min = 0;}
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {spw->sp_max = atoi(s);} else {spw->sp_max = 0;}
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {spw->sp_warn = atoi(s);} else {spw->sp_warn = 0;}
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {spw->sp_inact = atoi(s);} else {spw->sp_inact = 0;}
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {spw->sp_expire = atoi(s);} else {spw->sp_expire = 0;}
    //    printf(s);

        s = strtok (NULL,"\n");
        if (s!=NULL) {spw->sp_flag = atoi(s);} else {spw->sp_flag = 0;}
    //    printf(s);

        *errnop = 0;

        return NSS_STATUS_SUCCESS;
    }
    else
    {
        *errnop = ENOENT;
//        printf("User not found...\n");
        return NSS_STATUS_NOTFOUND;
    }

}
