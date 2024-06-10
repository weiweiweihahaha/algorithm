import time

import numpy as np


class Node:
    def __init__(self, name, arc_dict):
        self.name = name
        self.arc_dict = arc_dict


def create_node(name, next_list, flow_list):
    arc_dict = {}
    for i in range(len(next_list)):
        arc_dict[next_list[i]] = flow_list[i]
    return Node(name, arc_dict)


def create_level_graph(s, e, node_list, name_index_dict):
    level_graph = np.zeros((len(node_list), len(node_list))).tolist()
    cur_layer = [s]
    all_node = set()
    all_node.add(s)
    next_layer = set()
    while len(cur_layer) > 0:
        for node_name in cur_layer:
            node = node_list[name_index_dict[node_name]]
            for key in node.arc_dict.keys():
                if key not in all_node and (node.arc_dict[key] is None or node.arc_dict[key] > 0):
                    level_graph[name_index_dict[node_name]][name_index_dict[key]] = node.arc_dict[key]
                    next_layer.add(key)
                    all_node.add(key)
        cur_layer = list(next_layer)
        next_layer = set()
    return level_graph if e in all_node else None


def Dinic_Solve(s, e, node_list, name_index_dict):
    routes = []
    max_flow=0
    s_index = name_index_dict[s]
    e_index = name_index_dict[e]
    level_graph = create_level_graph(s, e, node_list, name_index_dict)
    while level_graph is not None:
        res_list = []
        while True:
            res = dfs(e_index, [s_index], None, level_graph)
            if res is None:
                break
            # 更新 level graph
            route, flow = res
            for i in range(len(route) - 1):
                if level_graph[route[i]][route[i + 1]] is not None:
                    level_graph[route[i]][route[i + 1]] -= flow
            # 追加记录增广路径
            res_list.append(res)
            routes.append([[node_list[n].name for n in res[0]], res[1]])
        # 更新残存网络
        for res in res_list:
            update(res, node_list)
        # 重新构造 level graph
        level_graph = create_level_graph(s, e, node_list, name_index_dict)
        max_flow += flow
    return routes,max_flow


def update(res, node_list):
    route, flow = res
    for i in range(len(route) - 1):
        n1 = node_list[route[i]]
        n2 = node_list[route[i + 1]]
        # 正向更新 n1 -> n2 剩余流量减少
        if n2.name in n1.arc_dict.keys() and n1.arc_dict[n2.name] is not None:
            n1.arc_dict[n2.name] = n1.arc_dict[n2.name] - flow
        # 反向更新 n2 -> n1 剩余流量增加
        if n1.name in n2.arc_dict.keys() and n2.arc_dict[n1.name] is not None:
            n2.arc_dict[n1.name] = n2.arc_dict[n1.name] + flow


def dfs(e_index, cur_route, last_flow, level_graph):
    if cur_route[-1] == e_index:
        return cur_route, last_flow
    for next_node in range(len(level_graph)):
        if next_node not in cur_route:
            if level_graph[cur_route[-1]][next_node] is None or level_graph[cur_route[-1]][next_node] > 0:
                flow = min_flow(level_graph[cur_route[-1]][next_node], last_flow)
                cur_route.append(next_node)
                res = dfs(e_index, cur_route, flow, level_graph)
                if res is not None:
                    return res
                cur_route.pop(-1)


def min_flow(f1, f2):
    '''
    求两个流量的较小者
    '''
    if f1 is None:
        return f2
    elif f2 is None:
        return f1
    else:
        return min(f1, f2)


if __name__ == '__main__':
    # 格式: [节点名, 后继节点的名称, 当前节点到各个后继的流量] （None 代表流量无穷大）
    graph1 = [
        ["S", ["1", "2", "3"], [5, 6, 8]],
        ["1", ["4"], [1]],
        ["2", ["4", "6"], [1, 1]],
        ["3", ["5"], [1]],
        ["4", ["E"], [1]],
        ["5", ["E"], [1]],
        ["6", ["E"], [1]],
        ["E", [], []]
    ]
    graph = [
        ["S", ["1", "2", "3", "4"], [3, 3, 3, 3]],  # Source node
        ["1", ["5", "6", "7", "8"], [1, 1, 1, 1]],
        ["2", ["6", "7", "8", "9"], [1, 1, 1, 1]],
        ["3", ["7", "8", "9", "10"], [1, 1, 1, 1]],
        ["4", ["8"], [1]],
        ["5", ["E"], [1]],
        ["6", ["E"], [1]],
        ["7", ["E"], [1]],
        ["8", ["E"], [1]],
        ["9", ["E"], [1]],
        ["10", ["E"], [1]],
        ["E", [], []]  # Sink node
    ]
    graph3 = [
        ["S", ["1", "2"], [11, 12]],  # Source node
        ["1", ["3"], [12]],
        ["2", ["1", "4"], [1, 11]],
        ["3", ["5"], [19]],
        ["4", ["3", "E"], [7, 4]],
        ["E", [], []]  # Sink node
    ]

    name_index_dict = dict()
    node_list = []
    for i in range(len(graph)):
        node_list.append(create_node(graph[i][0], graph[i][1], graph[i][2]))
        name_index_dict[graph[i][0]] = i

    # 记录算法开始时间
    start_time = time.perf_counter()

    # 调用算法求解最大流
    routes,max_flow = Dinic_Solve("S", "E", node_list, name_index_dict)

    # 记录算法结束时间
    end_time = time.perf_counter()

    # 计算算法运行时间
    elapsed_time = (end_time - start_time)*1000

    for i, (route, flow) in enumerate(routes):
        print(f"Route-{i + 1}: {route} , flow: {flow}")

    print(f"算法运行时间: {elapsed_time:.6f} ms", f"最大流为: {max_flow:f} ")

