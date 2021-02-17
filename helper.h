#ifndef _OPENMP

#include <time.h>
#define omp_get_wtime __get_time
#define omp_get_max_threads() 1
inline double __get_time()
{
    struct timespec tmp;
    clock_gettime(CLOCK_REALTIME, &tmp);
    double sec = (double)tmp.tv_sec;
    sec += ((double)tmp.tv_nsec) * 1E-9;
    return sec;
}

#else
#include <omp.h>
#endif

#define BEGIN_HOOK(NAME) double hook_start_##NAME = omp_get_wtime();
#define END_HOOK(NAME) printf("HOOK: %s requires %f seconds with %d max # of threads\n", \
                              #NAME,                                                     \
                              omp_get_wtime() - hook_start_##NAME,                       \
                              omp_get_max_threads());
