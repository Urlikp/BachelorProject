import numpy as np
from copy import deepcopy
from queue import Queue

nodeCount: int
faceCount: int
facesFound: int = 0
Edges: list
Neighbours: list


def swap_representation(face: list, swapped_representation: np.ndarray) -> np.ndarray:
    representation = deepcopy(swapped_representation)

    for node_1, node_2 in zip(reversed(face), reversed(range(len(face)))):
        representation[:, [node_1, node_2]] = representation[:, [node_2, node_1]]

    return representation


def save_representation(face: list, face_representation: np.ndarray, remaining_representation: np.ndarray):
    swapped_representation = np.append(face_representation, remaining_representation, axis=1)
    representation = np.transpose(swap_representation(face, swapped_representation))

    with open("input_representation.txt", "w") as RepresentationFile:
        for coordinates in representation:
            RepresentationFile.write(str(coordinates[0]) + " " + str(coordinates[1]) + "\n")


def compute_remaining_representation(face: list, face_representation: np.ndarray, laplacian_matrix: np.ndarray) -> np.ndarray:
    face_length = len(face)
    matrix_b = laplacian_matrix[:face_length, face_length:]
    remaining_laplacian_matrix = laplacian_matrix[face_length:, face_length:]
    remaining_representation = (-face_representation @ matrix_b @ np.linalg.inv(remaining_laplacian_matrix)).round(3)

    return remaining_representation


def swap_graph(face: list) -> list:
    swapped_edges = deepcopy(Edges)

    for node_1, node_2 in zip(face, range(len(face))):
        for edge in swapped_edges:
            if node_1 in edge and node_2 in edge:
                continue
            elif node_1 in edge:
                edge[edge.index(node_1)] = node_2
            elif node_2 in edge:
                edge[edge.index(node_2)] = node_1

    swapped_neighbours = [[] for _ in range(nodeCount)]

    for node in range(nodeCount):
        for edge in swapped_edges:
            if node in edge:
                swapped_neighbours[node].append(edge[not edge.index(node)])

    return swapped_neighbours


def create_laplacian_matrix(face: list) -> np.ndarray:
    swapped_neighbours = swap_graph(face)

    neighbour_count = [len(node_neighbours) for node_neighbours in swapped_neighbours]
    degree_matrix = np.eye(nodeCount, dtype=np.int64) * np.array(neighbour_count)

    adjacency_matrix = np.zeros((nodeCount, nodeCount), dtype=np.int64)

    for node in range(nodeCount):
        adjacency_matrix[node, swapped_neighbours[node]] = 1

    laplacian_matrix = degree_matrix - adjacency_matrix

    return laplacian_matrix


def compute_face_representation(face: list) -> np.ndarray:
    face_angles = len(face)

    face_coordinates = 0.9 * np.array(
        [np.cos(np.arange(face_angles, dtype=np.float64) * 2 * np.pi / face_angles).round(3),
         np.sin(np.arange(face_angles, dtype=np.float64) * 2 * np.pi / face_angles).round(3)]
    )

    return face_coordinates


def find_longest_face(faces: list) -> list:
    face_lengths = [len(face) for face in faces]
    longest_face = list(faces[np.argmax(face_lengths)])
    return longest_face


def bfs(starting_node: int, current_node: int, parents: list, faces_found: list, faces: set, node_queue: Queue):
    if starting_node == current_node and len(parents):
        faces_size = len(faces)
        faces.add(frozenset(parents))

        if len(faces) != faces_size:
            global facesFound
            facesFound += 1

            for parent in parents:
                faces_found[parent] += 1

        # if node_queue.empty():
        #     return
        # next_node, parent_nodes = node_queue.get()
        # bfs(starting_node, next_node, parent_nodes, faces_found, faces, node_queue)
        return

    if current_node in parents:
        if node_queue.empty():
            return
        next_node, parent_nodes = node_queue.get()
        bfs(starting_node, next_node, parent_nodes, faces_found, faces, node_queue)
        return

    parents.append(current_node)

    for neighbour in Neighbours[current_node]:
        if (len(parents) >= 2 and neighbour == parents[-2]) or neighbour < starting_node:
            continue
        parents_copy = deepcopy(parents)
        node_queue.put((neighbour, parents_copy))

    if node_queue.empty():
        return
    next_node, parent_nodes = node_queue.get()
    bfs(starting_node, next_node, parent_nodes, faces_found, faces, node_queue)


def find_faces() -> list:
    parents = []
    faces_found = [0] * nodeCount
    node_degrees = [len(node_neighbours) for node_neighbours in Neighbours]
    faces = set()

    node_queue = Queue()

    for node in range(nodeCount):
        if faces_found[node] < node_degrees[node]:
            bfs(node, node, parents, faces_found, faces, node_queue)
            node_queue.queue.clear()
            parents.clear()
            # print(f"Node {node}: ")
            # print(faces)

    # print("----------------------------------------------")
    # print(faces)
    # print(faces_found)
    # print(node_degrees)

    faces = list(faces)

    return faces


def load_graph():
    with open('input_graph.txt') as GraphFile:
        global nodeCount
        nodeCount = [int(x) for x in next(GraphFile).split()][0]
        global Edges
        Edges = [[int(x) for x in line.split()] for line in GraphFile]
        global faceCount
        faceCount = 2 - nodeCount + len(Edges)
        global Neighbours
        Neighbours = [[] for _ in range(nodeCount)]

        for node in range(nodeCount):
            for edge in Edges:
                if node in edge:
                    Neighbours[node].append(edge[not edge.index(node)])


def main():
    print("Hello, Algebraic Graph Theory!")
    load_graph()
    faces = find_faces()
    # print(faces)
    main_face = find_longest_face(faces)
    # print(main_face)
    main_face_representation = compute_face_representation(main_face)
    # print(main_face_representation)
    laplacian_matrix = create_laplacian_matrix(main_face)
    # print(laplacian_matrix)
    remaining_representation = compute_remaining_representation(main_face, main_face_representation, laplacian_matrix)
    # print(remaining_representation)
    save_representation(main_face, main_face_representation, remaining_representation)


if __name__ == "__main__":
    main()
