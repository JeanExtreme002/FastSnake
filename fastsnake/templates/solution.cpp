#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cmath>
#include <cstring>
#include <errno.h>
#include <functional>
#include <iomanip>
#include <iostream>
#include <list>
#include <map>
#include <numeric>
#include <queue>
#include <random>
#include <set>
#include <vector>

using namespace std;

#define int long long
#define double long double
#define float double

#define endl '\n'                            // Speed up output with line break

#define all(x) x.begin(), x.end()            // Example: sort(all(your_vector))
#define reverse_all(x) x.rbegin(), x.rend()  // Example: sort(reverse_all(your_vector))

void solve();

signed main() {
    // Optimizations to speed up input and output.
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    solve();

    return 0;
}

// const int mod = int(1e9) + 7; 
const int mod = 998244353;

int lcm(int a, int b){
    return a /__gcd(a, b) * b;
}

// =============================================================================
template <typename T> vector<T> put_array(int n) { 
    vector<T> vec(n);

    for (T &i: vec) {
        cin >> i;
    }

    return vec;
}

template <typename T> vector<vector<T>> put_matrix(int rows, int columns) { 
    vector<vector<T>> vec;

    for (int x = 0; x < rows; x++) {
        vector<T> vec2(columns);

        for (T &i: vec2) {
            cin >> i;
        }
        vec.push_back(vec2);
    }

    return vec;
}

string put() { 
    string var;
    cin >> var;
    return var;
}

int puti() { 
    int var;
    cin >> var;
    return var;
}

float putf() { 
    float var;
    cin >> var;
    return var;
}
// =============================================================================

#define puta(n) put_array<int>(n)        // You may use any other type here.
#define putm(n, m) put_matrix<int>(n, m) // You may use any other type here.
#define matrix vector<vector<int>>       // Do NOT forget to change the type here.

// >>> HEY, RIGHT HERE!! Write your code below:
// Remember, sometimes the solution is much simpler than you think S2
void solve() {
    int test_case = 1;
    cin >> test_case;

    while (test_case--) {
        int n = puti();
        // ...
    }
}


