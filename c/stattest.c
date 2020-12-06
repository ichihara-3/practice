#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <time.h>

int main(int argc, char **argv) {
  struct stat stat_buf;
  if (argc != 2) {
    fprintf(stderr, "main: invalid arguments\n");
    exit(EXIT_FAILURE);
  }
  const char *path = *(argv + 1);

  stat(path, &stat_buf);
  printf("%d dev_t    st_dev;    /* device inode resides on */\n",
         stat_buf.st_dev);
  printf("%llo ino_t    st_ino;    /* inode's number */\n", stat_buf.st_ino);
  printf("%d mode_t   st_mode;   /* inode protection mode */\n",
         stat_buf.st_mode);
  printf("%d nlink_t  st_nlink;  /* number of hard links to the file */\n",
         stat_buf.st_nlink);
  printf("%d uid_t    st_uid;    /* user-id of owner */\n", stat_buf.st_uid);
  printf("%d gid_t    st_gid;    /* group-id of owner */\n", stat_buf.st_gid);
  printf("%d dev_t    st_rdev;   /* device type, for special file inode */\n",
         stat_buf.st_gid);
  printf("%s struct timespec st_atimespec;  /* time of last access */\n",
         ctime(&stat_buf.st_atimespec.tv_sec));
  printf(
      "%s struct timespec st_mtimespec;  /* time of last data modification "
      "*/\n",
      ctime(&stat_buf.st_mtimespec.tv_sec));
  printf(
      "%s struct timespec st_ctimespec;  /* time of last file status change "
      "*/\n",
      ctime(&stat_buf.st_ctimespec.tv_sec));
  printf("%lld off_t    st_size;   /* file size, in bytes */\n",
         stat_buf.st_size);
  printf("%lld quad_t   st_blocks; /* blocks allocated for file */\n",
         stat_buf.st_blocks);
  printf("%d u_long   st_blksize;/* optimal file sys I/O ops blocksize */\n",
         stat_buf.st_blksize);
  printf("%d u_long   st_flags;  /* user defined flags for file */\n",
         stat_buf.st_flags);
  printf("%d u_long   st_gen;    /* file generation number */\n",
         stat_buf.st_gen);
}
