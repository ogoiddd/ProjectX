import java.util.*;

class BestFirst {
    protected Queue<State> abertos;
    private Map<Ilayout, State> fechados;
    private State actual;
    private Ilayout objective;

    static class State {
        private Ilayout layout;
        private State father;
        private double g;

        public State(Ilayout l, State n) {
            layout = l;
            father = n;
            if (father != null)
                g = father.g + l.getK();
            else g = 0.0;
        }

        public String toString() { return layout.toString(); }
        public double getG() { return g; }
        public int hashCode() { return toString().hashCode(); }

        public boolean equals(Object o) {
            if (o == null) return false;
            if (this.getClass() != o.getClass()) return false;
            State n = (State) o;
            return this.layout.equals(n.layout);
        }
    }

    final private List<State> sucessores(State n) {
        List<State> sucs = new ArrayList<>();
        List<Ilayout> children = n.layout.children();
        for (Ilayout e : children) {
            if (n.father == null || !e.equals(n.father.layout)) {
                State nn = new State(e, n);
                sucs.add(nn);
            }
        }
        return sucs;
    }

    /** Path from the initial state to n, in that order. */
    private Iterator<State> path(State n) {
        LinkedList<State> path = new LinkedList<>();
        for (State s = n; s != null; s = s.father)
            path.addFirst(s);
        return path.iterator();
    }

    final public Iterator<State> solve(Ilayout s, Ilayout goal) {
        objective = goal;
        abertos = new PriorityQueue<>(10,
            (s1, s2) -> (int) Math.signum(s1.getG() - s2.getG()));
        fechados = new HashMap<>();
        abertos.add(new State(s, null));
        // Configurations already in abertos; together with fechados this tells
        // whether a successor was "presented before" in O(1).
        Set<Ilayout> emAbertos = new HashSet<>();
        emAbertos.add(s);
        List<State> sucs;
        while (true) {
            if (abertos.isEmpty()) return null;
            actual = abertos.remove();
            emAbertos.remove(actual.layout);
            if (actual.layout.isGoal(objective))
                return path(actual);
            sucs = sucessores(actual);
            fechados.put(actual.layout, actual);
            for (State suc : sucs) {
                if (!fechados.containsKey(suc.layout) && !emAbertos.contains(suc.layout)) {
                    abertos.add(suc);
                    emAbertos.add(suc.layout);
                }
            }
        }
    }
}
