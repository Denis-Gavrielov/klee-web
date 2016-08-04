/*
 * First KLEE tutorial: testing a small function
 * http://klee.github.io/tutorials/testing-function/
 */


int get_sign(int x) {
	if (x == 0)
		return 0;

	if (x < 0)
		return -1;
	else
		return 1;
}

int main() {
	int a;
	klee_make_symbolic(&a, sizeof(a), "a");
	return get_sign(a);
}