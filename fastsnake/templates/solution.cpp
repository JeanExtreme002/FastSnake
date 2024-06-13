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
#include <sstream>
#include <string>
#include <vector>

using namespace std;

#define int long long
#define double long double
#define float double

#define endl '\n'                                           // Speed up output with line break

#define all(x) x.begin(), x.end()                           // Example: sort(all(your_vector))
#define all_reversed(x) x.rbegin(), x.rend()                // Example: sort(all_reversed(your_vector))

#define ceil_div(a, b) floor((a + b - 1) / b)               // Example: ceil_div(10, 3) == 4

void solve();

signed main() {
    // Optimizations to speed up input and output.
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    solve();

    return 0;
}

// [String Functions]: ==========================================================
vector<string> split(const string &str, char delimiter = ' ') {
    vector<string> tokens;
    string token;
    stringstream ss(str);

    while (getline(ss, token, delimiter)) {
        tokens.push_back(token);
    }
    return tokens;
}

// [Slice Functions]: ==========================================================
template <typename T> vector<T> slice(vector<T> &vec, int start, int end, int step = 1) {
    if (step == 0 || (step > 0 && start >= end) || (step < 0 && start <= end)) {
        vector<T> v_empty(0);
        return v_empty;
    }

    int size = floor((abs(end - start) + abs(step) - 1) / abs(step));

    vector<T> c_vec(size);

    for (int i = 0; i < size; i++) {
        int index = start + (i * step);
        c_vec[i] = vec[index];
    }

    return c_vec;
}

string slice(string &str, int start, int end, int step = 1) {
    if (step == 0 || (step > 0 && start >= end) || (step < 0 && start <= end)) {
        string str_empty = "";
        return str_empty;
    }

    int size = floor((abs(end - start) + abs(step) - 1) / abs(step));

    char c_str[size + 1];

    for (int i = 0; i < size; i++) {
        int index = start + (i * step);
        c_str[i] = str[index];
    }

    c_str[size] = '\0';
    
    string final_c_str(c_str);
    return final_c_str;
}

// [Print Functions]: ==========================================================
template <typename T> void println(T t) { cout << t << endl; }

template <typename T, typename ... U> void println(T t, U ... u) {
    cout << t << ' ';
    println(u ...);
}

template <typename T> void println(vector<T> vec) {
    for (int i = 0; i < vec.size() - 1; i++) {
        cout << vec[i] << ' ';
    }
    if (vec.size() > 0) {
        cout << vec[vec.size() - 1];
    }
    cout << endl;
}

template <typename T> void println(set<T> s) {
  set<int>::iterator itr;
  int count = 0;
    
  for (itr = s.begin(); itr != s.end(); itr++) {
    cout << *itr;

    if (++count == s.size()) {
        cout << endl;
    }
    else {
        cout << ' ';
    }
  }
}  

void println() { cout << endl; }

template <typename T> void print(T t) { cout << t; }

template <typename T, typename ... U> void print(T t, U ... u) {
    cout << t << ' ';
    print(u ...);
}

// [Input Functions]: ==========================================================
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

const int mod = 998244353; // int(1e9) + 7; 

int lcm(int a, int b){
    return a /__gcd(a, b) * b;
}

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


