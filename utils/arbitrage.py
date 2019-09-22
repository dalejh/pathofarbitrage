from typing import Tuple, List, Union


def convert_back(curr, start, gph, total) -> List[Union[float, int]]:
    ttl = total
    fx = 0
    for tupe in gph[curr]:
        if tupe[1] == start:
            fx = tupe[2]
            ttl = ttl * fx
    return [ttl, curr, start, fx]


'''
Brute force arbitrage computation -- cycles between vertices are permitted as parallel edges have different weights.
todo: refactor into better data structure.
'''


def find_max(g, start_amount, vertex, dep) -> Tuple[float, List[List[Union[int, float]]]]:
    total = start_amount
    start_node = vertex
    path = []

    for depth in range(dep):
        best_trades_at_depth = []

        for tup in g[start_node]:

            current_comparison_node = tup[1]
            current_node = start_node
            fx = tup[2]
            # print(f'{total} {current_node} orbs to {current_comparison_node} orbs is {total * fx}')
            potential_total = total * fx
            potential_trade = convert_back(current_comparison_node, current_node, g, potential_total)

            if potential_trade[0] > total:
                profit = potential_trade[0] - total
                for tp in g[current_node]:
                    if tp[1] == 4:
                        profit *= tp[2]
                # print(f'PROFIT IN CHAOS ORBS: {profit:.2f}')
                # print(f'verified trade: {total:.2f} {current_node} orbs to {current_comparison_node} orbs is {total * fx:.2f}')
                verified_trade = [profit, total * fx, current_comparison_node, current_node]
                # print('potential', verified_trade)
                best_trades_at_depth.append(verified_trade)

        best_trades_at_depth.sort(reverse=True)
        if best_trades_at_depth:
            # print('hit', best_trades_at_depth)
            start_node = best_trades_at_depth[0][2]
            pre_total = total
            total = best_trades_at_depth[0][1]
            path.append([pre_total, best_trades_at_depth[0][3], best_trades_at_depth[0][2], total])
            # print(f'start is now node {start_node}, total is now {total:.2f}')
    # print()
    # print(f'path is {path}')
    # print(total)
    # print(f'profit is {(total - start_amount):.2f} orbs')
    return path


graph = {1: [(1, 4, 0.12680135046550284), (1, 6, 0.0007474473670754143), (1, 7, 1.1159064327485382)],
         4: [(4, 1, 10.212), (4, 6, 0.005820990657508266), (4, 7, 14.464109475430229)],
         6: [(6, 1, 1223.2), (6, 4, 176.13333333333333), (6, 7, 1972.0)],
         7: [(7, 1, 0.7210875303558231), (7, 4, 0.08228435189584501), (7, 6, 0.00041333333333333337)]}

graph_two = {1: [(1, 2, 0.18067595459236327), (1, 3, 0.18504773037210206), (1, 4, 0.13470496134279797), (1, 5, 0.07105152261183934), (1, 6, 0.0007391313859101863)],
             2: [(2, 1, 4.2), (2, 3, 0.9267734553775744), (2, 4, 0.4970562386501844), (2, 5, 0.34022988505747126), (2, 6, 0.002771639042357274)],
             3: [(3, 1, 4.8), (3, 2, 1.0), (3, 4, 0.4994999576803171), (3, 5, 0.36363636363636365), (3, 6, 0.002560943300117184)],
             4: [(4, 1, 9.9), (4, 2, 2.079769572576731), (4, 3, 2.1313406593406596), (4, 5, 1.005128205128205), (4, 6, 0.0057339901477832505)],
             5: [(5, 1, 9.074545454545454), (5, 2, 1.9166666666666667), (5, 3, 1.8047058823529412), (5, 4, 1.004), (5, 6, 0.005449744675551128)],
             6: [(6, 1, 1300.8), (6, 2, 367.6666666666667), (6, 3, 374.2), (6, 4, 176.7333333333333), (6, 5, 183.2)]}

graph_three = {1: [(1, 2, 0.18138183694530446), (1, 3, 0.1683810637054354), (1, 4, 0.14245472837022133), (1, 5, 0.07131608548931383), (1, 6, 0.000770771511469117), (1, 7, 1.03), (1, 8, 0.7722450923689314), (1, 9, 0.29256198347107437), (1, 10, 0.23675651983344287)],
               2: [(2, 1, 4.0), (2, 3, 0.8646616541353384), (2, 4, 0.5005025125628141), (2, 5, 0.34022988505747126), (2, 6, 0.0028092303529397545), (2, 7, 4.885), (2, 8, 3.7284057971014497), (2, 9, 1.41), (2, 10, 1.3038095238095238)],
               3: [(3, 1, 4.95), (3, 2, 1.0), (3, 4, 0.4991093739688378), (3, 5, 0.36363636363636365), (3, 6, 0.0025409155800894642), (3, 7, 4.8090909090909095), (3, 8, 3.8136904761904757), (3, 9, 1.625), (3, 10, 1.8)],
               4: [(4, 1, 8.337272727272728), (4, 2, 2.013683482570083), (4, 3, 2.1268791208791207), (4, 5, 1.018), (4, 6, 0.00580762524719017), (4, 7, 13.232766805266806), (4, 8, 8.160042553191488), (4, 9, 8.386363636363637), (4, 10, 3.209057471264368)],
               5: [(5, 1, 8.654545454545454), (5, 2, 1.9333333333333336), (5, 3, 1.844705882352941), (5, 4, 1.0033898305084745), (5, 6, 0.005411600895471864), (5, 7, 10.0), (5, 8, 7.142857142857143), (5, 9, 1.3), (5, 10, 3.3333333333333335)],
               6: [(6, 1, 1237.2), (6, 2, 370.4), (6, 3, 374.2), (6, 4, 177.06666666666666), (6, 5, 177.6), (6, 7, 1974.4), (6, 8, 1254.2), (6, 9, 1003.2), (6, 10, 588.6)],
               7: [(7, 1, 0.7270021645021645), (7, 2, 0.16807672221430944), (7, 3, 0.13431048551611585), (7, 4, 0.08638080079892643), (7, 5, 0.05371418689110509), (7, 6, 0.0004376568018511753), (7, 8, 0.8190852625635234), (7, 9, 0.2571428571428571), (7, 10, 0.22537787619139307)],
               8: [(8, 1, 0.9676923076923076), (8, 2, 0.24047619047619045), (8, 3, 0.1929620755184665), (8, 4, 0.12213240418118468), (8, 5, 0.06166046124927703), (8, 6, 0.0005907733332758898), (8, 7, 1.1219999999999999), (8, 9, 0.2836231884057971), (8, 10, 0.2864473448954049)],
               9: [(9, 1, 0.7538681318681318), (9, 2, 0.2054032258064516), (9, 3, 0.1991867612293144), (9, 4, 0.15140080045740423), (9, 5, 0.026666666666666665), (9, 6, 0.000700569638894275), (9, 7, 1.0), (9, 8, 0.8028399122807016), (9, 10, 0.19109461966604824)],
               10: [(10, 1, 2.3333333333333335), (10, 2, 0.5525525525525525), (10, 3, 0.44009081331647704), (10, 4, 0.3367621274108708), (10, 5, 0.2074829931972789), (10, 6, 0.0017570497183899008), (10, 7, 2.773333333333333), (10, 8, 2.2888888888888888), (10, 9, 0.8714285714285716)]}

graph_four = {1: [(1, 2, 0.17718384195783576), (1, 3, 0.1683810637054354), (1, 4, 0.14270382977720905), (1, 5, 0.06611422213527657),
                  (1, 6, 0.0007818897089728428), (1, 7, 1.0), (1, 8, 0.7754932126696833), (1, 10, 0.23640793595544726),
                  (1, 11, 0.146007326007326), (1, 13, 0.07904761904761903)],
              2: [(2, 1, 4.0), (2, 3, 0.8881987577639752),
                  (2, 4, 0.4998813945503917), (2, 5, 0.30414500442086645),
                  (2, 6, 0.002826486370934869), (2, 7, 4.79409090909091), (2, 8, 3.6866666666666665), (2, 10, 1.2914285714285714), (2, 11, 0.6681318681318681), (2, 13, 0.6818181818181818)],
              3: [(3, 1, 4.8), (3, 2, 1.0), (3, 4, 0.4993359614015026), (3, 5, 0.35757575757575755), (3, 6, 0.0025410036464374223), (3, 7, 4.677272727272728), (3, 8, 3.7851190476190473), (3, 10, 1.7971428571428572), (3, 11, 0.8911111111111112), (3, 13, 0.2666666666666667)],
              4: [(4, 1, 8.64), (4, 2, 2.4971365070231073), (4, 3, 2.166233158146201), (4, 5, 1.1480000000000001), (4, 6, 0.0058012170385395535), (4, 7, 13.741164241164242), (4, 8, 8.313333333333336), (4, 10, 3.2667272727272723), (4, 11, 2.493764705882353), (4, 13, 2.2095471698113207)],
              5: [(5, 1, 8.236363636363638), (5, 2, 1.9166666666666667), (5, 3, 1.8047058823529412), (5, 4, 1.0), (5, 6, 0.005255800792303339), (5, 7, 10.0), (5, 8, 6.95), (5, 10, 3.266666666666667), (5, 11, 1.3333333333333333), (5, 13, 1.0786363636363636)],
              6: [(6, 1, 1346.4), (6, 2, 371.0), (6, 3, 374.4), (6, 4, 177.86666666666667), (6, 5, 180.0), (6, 7, 2152.0), (6, 8, 1270.0), (6, 10, 599.0), (6, 11, 338.6), (6, 13, 382.0)],
              7: [(7, 1, 0.7207243867243868), (7, 2, 0.13513513513513514),
                  (7, 3, 0.13038009502375594), (7, 4, 0.08512205954018517), (7, 5, 0.0431878711016314), (7, 6, 0.0004242424242424243), (7, 8, 0.8190852625635234), (7, 10, 0.22070315862224624), (7, 11, 0.10766628901696138), (7, 13, 0.07272727272727272)],
              8: [(8, 1, 0.9714285714285713), (8, 2, 0.24047619047619045), (8, 3, 0.19506733867636125), (8, 4, 0.12213240418118468), (8, 5, 0.05304276315789473), (8, 6, 0.000605578093306288), (8, 7, 1.05), (8, 10, 0.2737792385467202), (8, 11, 0.10510337854328648), (8, 13, 0.11240103270223752)],
              10: [(10, 1, 2.3333333333333335), (10, 2, 0.5465465465465466), (10, 3, 0.4399955752212389), (10, 4, 0.34985617859066476), (10, 5, 0.22414965986394558), (10, 6, 0.001704339746404685), (10, 7, 2.76), (10, 8, 2.2488888888888887), (10, 11, 0.4684552845528455), (10, 13, 0.17777777777777776)],
              11: [(11, 1, 3.257142857142857), (11, 2, 0.9064935064935066), (11, 3, 0.8613240418118467), (11, 4, 0.5333333333333333), (11, 5, 0.15), (11, 6, 0.00282546126190194), (11, 7, 4.7595238095238095), (11, 8, 3.066666666666667), (11, 10, 1.2754367201426025), (11, 13, 0.5714285714285714)],
              13: [(13, 1, 4.602941176470589), (13, 2, 1.2430937256935441), (13, 3, 0.8145454545454547), (13, 4, 0.5), (13, 5, 0.35151515151515145), (13, 6, 0.002531944663523611), (13, 7, 4.80952380952381), (13, 8, 3.6666666666666665), (13, 10, 2.12), (13, 11, 0.8380952380952381)]}

if __name__ == '__main__':
    start_monies = 100
    search_depth = 3
    start_currency_ID = 4

    test1 = find_max(graph_four, start_monies, start_currency_ID, search_depth)
