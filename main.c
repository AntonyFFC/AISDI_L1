#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <time.h>

typedef struct {
    int* data;
    int size;
    int min_val;
    int max_val;
} ArrayData;

double find_median(ArrayData* arrays, int m) {
    int curr_min = INT_MAX;
    int curr_max = INT_MIN;
    long long total_count = 0;

    for (int i = 0; i < m; i++) {
        if (arrays[i].min_val < curr_min) curr_min = arrays[i].min_val;
        if (arrays[i].max_val > curr_max) curr_max = arrays[i].max_val;
        total_count += arrays[i].size;
    }

    long long target = (total_count + 1) / 2;

    while (curr_min <= curr_max) {
        int mid = curr_min + (curr_max - curr_min) / 2; 
        long long count_left = 0;

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < arrays[i].size; j++) {
                if (arrays[i].data[j] <= mid) {
                    count_left++;
                }
            }
        }

        if (count_left < target) {
            curr_min = mid + 1;
        } else {
            curr_max = mid - 1;
        }
    }

    if (total_count % 2 == 0) {
        long long count_left = 0;
        int next_min = INT_MAX;

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < arrays[i].size; j++) {
                if (arrays[i].data[j] <= curr_min) {
                    count_left++;
                } else if (arrays[i].data[j] > curr_min && arrays[i].data[j] < next_min) {
                    next_min = arrays[i].data[j];
                }
            }
        }

        if (count_left > target) {
            return (double)curr_min;
        } else {
            return ((double)curr_min + (double)next_min) / 2.0;
        }
    }

    return (double)curr_min;
}

int main() {
    int m = 20;
    ArrayData* arrays = malloc(m * sizeof(ArrayData));
    long long total_elements = 0;

    srand(time(NULL));

    printf("Generating random data in C...\n");
    for (int i = 0; i < m; i++) {
        int size = 10000 + rand() % 40001;
        arrays[i].size = size;
        arrays[i].data = malloc(size * sizeof(int));
        total_elements += size;

        int min_val = INT_MAX;
        int max_val = INT_MIN;

        for (int j = 0; j < size; j++) {
            int val = rand() % 10001;
            arrays[i].data[j] = val;
            if (val < min_val) min_val = val;
            if (val > max_val) max_val = val;
        }
        arrays[i].min_val = min_val;
        arrays[i].max_val = max_val;
    }

    printf("Generated %d arrays with %lld total elements.\n", m, total_elements);

    clock_t start_time = clock();
    double median_val = find_median(arrays, m);
    clock_t end_time = clock();

    double cpu_time = ((double) (end_time - start_time)) / CLOCKS_PER_SEC;

    printf("\n--- Results ---\n");
    printf("C Algorithm Median: %f\n", median_val);
    printf("C Algorithm Time:   %.6f seconds\n", cpu_time);

    for (int i = 0; i < m; i++) {
        free(arrays[i].data);
    }
    free(arrays);

    return 0;
}