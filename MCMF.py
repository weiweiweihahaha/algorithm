from collections import deque, defaultdict
import sys

# 常量定义
MAXN = 5050
INF = sys.maxsize


# 定义边的结构
class Edge:
    def __init__(self, from_, to, flow, cost):
        self.from_ = from_
        self.to = to
        self.flow = flow
        self.cost = cost


# 最小费用最大流类
class MCMF:
    def __init__(self, n):
        self.n = n
        self.edges = []
        self.head = [-1] * n
        self.next_edge = defaultdict(list)
        self.num_edge = 0
        self.maxFlow = 0
        self.minCost = 0

    # 添加边的方法
    def add_edge(self, from_, to, flow, cost):
        self.edges.append(Edge(from_, to, flow, cost))
        self.edges.append(Edge(to, from_, 0, -cost))
        self.num_edge += 2
        self.next_edge[from_].append(self.num_edge - 2)
        self.next_edge[to].append(self.num_edge - 1)

    # SPFA算法用于寻找最短路径
    def SPFA(self, s, t):
        cost = [INF] * self.n
        flow = [INF] * self.n
        vis = [False] * self.n
        pre = [-1] * self.n
        last = [-1] * self.n
        q = deque([s])
        vis[s] = True
        cost[s] = 0

        while q:
            now = q.popleft()
            vis[now] = False
            for i in self.next_edge[now]:
                e = self.edges[i]
                if e.flow > 0 and cost[e.to] > cost[now] + e.cost:
                    cost[e.to] = cost[now] + e.cost
                    pre[e.to] = now
                    last[e.to] = i
                    flow[e.to] = min(flow[now], e.flow)
                    if not vis[e.to]:
                        vis[e.to] = True
                        q.append(e.to)

        self.pre = pre
        self.last = last
        self.flow = flow
        self.cost = cost
        return pre[t] != -1

    # 运行最小费用最大流算法
    def run_mcmf(self, s, t):
        augment_paths = []  # 用于存储增广路径
        while self.SPFA(s, t):
            now = t
            augment_path = [t]  # 存储当前增广路径
            self.maxFlow += self.flow[t]
            self.minCost += self.flow[t] * self.cost[t]
            while now != s:
                self.edges[self.last[now]].flow -= self.flow[t]
                self.edges[self.last[now] ^ 1].flow += self.flow[t]
                now = self.pre[now]
                augment_path.append(now)
            augment_path.reverse()  # 将路径反转，以便从源点到汇点打印
            augment_paths.append(augment_path)
        return augment_paths, self.maxFlow, self.minCost

        # Cycle-Canceling算法
    def cycle_canceling(self, s, t):
        # 找到负环并取消
        while True:
            # 使用Bellman-Ford算法寻找负环
            dist = [0] * self.n
            for _ in range(self.n - 1):
                for e in self.edges:
                    if e.flow > 0 and dist[e.to] > dist[e.from_] + e.cost:
                        dist[e.to] = dist[e.from_] + e.cost
            # 判断是否存在负环
            neg_cycle = False
            for e in self.edges:
                if e.flow > 0 and dist[e.to] > dist[e.from_] + e.cost:
                    neg_cycle = True
                    break
            if not neg_cycle:
                break
            # 取消负环
            bottleneck = INF
            u = t
            while True:
                e = self.edges[self.last[u]]
                bottleneck = min(bottleneck, e.flow)
                u = e.from_
                if u == s:
                    break
            u = t
            while True:
                e = self.edges[self.last[u]]
                e.flow -= bottleneck
                self.edges[self.last[u] ^ 1].flow += bottleneck
                u = e.from_
                if u == s:
                    break
            self.maxFlow += bottleneck
            self.minCost += bottleneck * dist[t]
    def run_mcmf_with_cycle_canceling(self, s, t):
        augment_paths = []  # 用于存储增广路径
        self.cycle_canceling(s, t)  # 使用Cycle-Canceling算法
        return [], self.maxFlow, self.minCost
# 测试案例
import time


def main():
    n = 8  # 节点数
    s = 0  # 源点
    t = 7  # 汇点

    mcmf = MCMF(n)

    # 初始化边
    edges = [
        (0, 1, 10, 2),  # 起点，终点，容量，费用
        (0, 2, 5, 3),
        (1, 2, 15, 1),
        (1, 3, 10, 2),
        (2, 3, 10, 1),
        (2, 4, 10, 2),
        (3, 5, 15, 3),
        (4, 5, 5, 2),
        (4, 6, 10, 1),
        (5, 7, 10, 3),
        (6, 7, 10, 2)
    ]

    for u, v, c, w in edges:
        mcmf.add_edge(u, v, c, w)

    start_time = time.time()  # 记录开始时间

    augment_paths, maxFlow, minCost = mcmf.run_mcmf(s, t)



    end_time = time.time()  # 记录结束时间
    elapsed_time = (end_time - start_time) * 1000
    print("增广路径为：")
    for path in augment_paths:
        print("->".join(map(str, path)))
    print("最大流为：", maxFlow)
    print("最小费用为：", minCost)

    print(f"算法运行时间: {elapsed_time:.6f} ms")

    start_time = time.time()  # 记录开始时间
    for _ in range(1000):
        augment_paths, maxFlow, minCost = mcmf.run_mcmf_with_cycle_canceling(s, t)  # 使用 Cycle-Canceling 算法

    end_time = time.time()  # 记录结束时间

    print("\n使用 Cycle-Canceling 算法求解：")
    print("最大流为：", maxFlow)
    print("最小费用为：", minCost)
    print("执行时间为：", (end_time - start_time) * 1000, "ms")


if __name__ == "__main__":
    main()
