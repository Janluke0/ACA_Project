#ifndef __OMP_H
#include <time.h>
#define omp_get_wtime __get_time
#define omp_get_max_threads() 1
double __get_time()
{
    struct timespec tmp;
    clock_gettime(CLOCK_REALTIME, &tmp);
    double sec = (double)tmp.tv_sec;
    sec += ((double)tmp.tv_nsec) * 1E-9;
    return sec;
}
#endif

#define BEGIN_HOOK(NAME) double NAME_hook_start = omp_get_wtime();
#define END_HOOK(NAME) printf("%s requires %f seconds with %d max # of threads", \
                              #NAME,                                             \
                              omp_get_wtime() - NAME_hook_start,                 \
                              omp_get_max_threads());
