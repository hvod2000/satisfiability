#include <bits/stdc++.h>
using namespace std;

typedef vector<set<int>> graph_t;

const bool DEBUG = false;

vector<int> topological_order(graph_t &G) {
	int n = G.size();
	vector<bool> visited(n);
	vector<int> order(n);
	int unprocessed = n;
	function<void(int)>  dfs = [&](int u) {
		if (visited[u]) return;
		visited[u] = true;
		for (int v : G[u]) dfs(v);
		order[--unprocessed] = u;
	};
	for (int u = 0; u < n; u++) dfs(u);
	return order;
}

graph_t reversed_graph(graph_t &G) {
	int n = G.size();
	graph_t reversed(G.size());
	for (int u = 0; u < n; u++) for (int v : G[u]) reversed[v].insert(u);
	return reversed;
}

vector<set<int>> strongly_connected_components(graph_t &G) {
	vector<int> order = topological_order(G);
	vector<bool> visited(G.size());
	graph_t Grev = reversed_graph(G);
	vector<set<int>> components;
	function<void(int)> dfs = [&](int u) {
		if (visited[u]) return;
		visited[u] = true;
		for (int v : Grev[u]) dfs(v);
		components[components.size() - 1].insert(u);
	};
	for (int u : order) {
		if (not visited[u]) {
			set<int> empty;
			components.push_back(empty);
			dfs(u);
		}
	}
	return components;
}

vector<set<int>> stretch(graph_t &G, vector<set<int>> &components) {
	int n = G.size();
	int new_n = components.size();
	vector<int> vert2comp(n);
	for (int comp = 0; comp < new_n; comp++)
		for (int u : components[comp])
			vert2comp[u] = comp;
	graph_t result(new_n);
	for (int u = 0; u < n; u++)
		for (int v : G[u]) {
			int U = vert2comp[u], V = vert2comp[v];
			if (U == V) continue;
			result[U].insert(V);
		}
	return result;
}

bool eval(string quantifiers, vector<set<int>> &G) {
	int n = G.size() / 2;
	vector<set<int>> components = strongly_connected_components(G);
	vector<int> vert2comp(n * 2);
	for (int comp = 0; comp < components.size(); comp++)
		for (int u : components[comp])
			vert2comp[u] = comp;
	graph_t g = stretch(G, components);
	vector<int> order = topological_order(g);
	reverse(order.begin(), order.end());
	vector<bool> has_universals(g.size());
	for (int u : order) {
		// S = ~S
		if (u == vert2comp[(*components[u].begin() + n) % (2 * n)]) return false;
		// ExAy : (x = y)
		int first_existential = 0x7fffffff;
		int last_universal = 0;
		for (int x : components[u])
			if (quantifiers[x % n] == 'A') last_universal = max(last_universal, x % n);
			else first_existential = min(first_existential, x % n);
		if (first_existential < last_universal) return false;
		// AxAy : (x -> y)
		int unis = 0;
		for (int x : components[u])
			if (quantifiers[x % n] == 'A')
				unis += 1;
		if (unis >= 2) return false;
		has_universals[u] = unis;
		for (int v : g[u]) if (unis + has_universals[v] >= 2) return false;
		for (int v : g[u]) unis = unis or has_universals[v];
		has_universals[u] = unis;
	}
	return true;
}


int main() {
	int n, m;
	cout << "Input number of variables: ";
	cin >> n;
	cout << "Input number of clauses: ";
	cin >> m;
	string quantifiers;
	cout << "Input quantifiers: ";
	cin >> quantifiers;
	cout << "Input clauses one by one" << endl;
	vector<set<int>> implication_graph(n * 2);
	for (int t = 0; t < m; t++) {
		int u, v;
		cin >> u >> v;
		u = (u > 0) ? (u - 1) : (n - u - 1);
		v = (v > 0) ? (v - 1) : (n - v - 1);
		implication_graph[(u + n)%(2*n)].insert(v);
		implication_graph[(v + n)%(2*n)].insert(u);
	}
	bool result = eval(quantifiers, implication_graph);
	cout << result << endl;
}
