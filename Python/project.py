import numpy as np
from copy import deepcopy
from queue import Queue
from sys import argv


class Graph:
    """	docstring for Graph """

    def __init__(self):
        self.nodeCount: int = 0
        self.faceCount: int = 0
        self.facesFound: int = 0
        self.Edges: list = []
        self.Neighbours: list = []

    def main(
            self, main_face: list = None, graph_file: str = "input_graph.txt",
            representation_file: str = "input_representation.txt",
            random_representation_file: str = "input_random_representation.txt"
    ) -> None:
        """
        :param main_face:
        :param graph_file: path to file containing graph (default input_graph.txt)
        :param representation_file: path to created file containing generated coordinates (default input_representation.txt)
        :param random_representation_file:
        :return: None
        """
        print("Hello, Algebraic Graph Theory!")
        self.load_graph(graph_file)

        if main_face is None:
            faces = self.find_faces()
            main_face = self.find_longest_face(faces)

        main_face_representation = self.compute_face_representation(main_face)
        laplacian_matrix = self.create_laplacian_matrix(main_face)
        remaining_representation = self.compute_remaining_representation(
            main_face, main_face_representation, laplacian_matrix
        )
        random_remaining_representation = self.generate_random_remaining_representation(
            main_face, main_face_representation
        )
        self.save_representation(
            representation_file, random_representation_file, main_face, main_face_representation,
            remaining_representation, random_remaining_representation
        )

    def load_graph(self, graph_file: str) -> None:
        """
        File must be in form:\n
        Line1: N (integer, number of nodes)\n
        Line2: A B (node A is connected with node B, A and B are integers)\n
        ...\n
        Last_Line: X Y

        :param graph_file: containing graph connections
        :return: None
        """
        print(f"Loading graph connection from: {graph_file}")

        assert (graph_file is not None)
        with open(graph_file, "r") as GraphFile:
            # --------------- Init ---------------
            self.nodeCount = [int(x) for x in next(GraphFile).split()][0]
            self.Edges = [[int(x) for x in line.split()] for line in GraphFile]
            self.faceCount = 2 - self.nodeCount + len(self.Edges)
            self.Neighbours = [[] for _ in range(self.nodeCount)]

        for node in range(self.nodeCount):
            for edge in self.Edges:
                if node in edge:
                    self.Neighbours[node].append(edge[not edge.index(node)])

    def find_faces(self) -> list:
        """
        :return:
        """
        parents = []
        faces_found = [0] * self.nodeCount
        node_degrees = [len(node_neighbours) for node_neighbours in self.Neighbours]
        faces = []

        node_queue = Queue()

        for node in range(self.nodeCount):
            if faces_found[node] < node_degrees[node]:
                self.bfs(node, node, parents, faces_found, faces, node_queue)
                node_queue.queue.clear()
                parents.clear()

        return faces

    def bfs(
            self, starting_node: int, current_node: int, parents: list, faces_found: list, faces: list,
            node_queue: Queue
    ) -> None:
        """
        :param starting_node: starting node (index)
        :param current_node: current node (index)
        :param parents:
        :param faces_found:
        :param faces:
        :param node_queue: queue of nodes
        :return: None
        """
        if starting_node == current_node and len(parents):
            faces_size = len(faces)
            faces.append(parents)

            if len(faces) != faces_size:
                self.facesFound += 1

                for parent in parents:
                    faces_found[parent] += 1
            return

        if current_node in parents:
            if node_queue.empty():
                return
            next_node, parent_nodes = node_queue.get()
            self.bfs(starting_node, next_node, parent_nodes, faces_found, faces, node_queue)
            return

        parents.append(current_node)

        for neighbour in self.Neighbours[current_node]:
            if (len(parents) >= 2 and neighbour == parents[-2]) or neighbour < starting_node:
                continue
            parents_copy = deepcopy(parents)
            node_queue.put((neighbour, parents_copy))

        if node_queue.empty():
            return
        next_node, parent_nodes = node_queue.get()
        self.bfs(starting_node, next_node, parent_nodes, faces_found, faces, node_queue)

    def find_longest_face(self, faces: list) -> list:
        """
        :param faces:
        :return:
        """
        face_lengths = [len(face) for face in faces]
        longest_face = faces[np.argmax(face_lengths)]

        return longest_face

    def compute_face_representation(self, face: list) -> np.ndarray:
        """
        :param face:
        :return:
        """
        face_angles = len(face)

        face_coordinates = 0.9 * np.array([
                np.cos(np.arange(face_angles, dtype=np.float64) * 2 * np.pi / face_angles).round(3),
                np.sin(np.arange(face_angles, dtype=np.float64) * 2 * np.pi / face_angles).round(3)
        ])

        return face_coordinates

    def create_laplacian_matrix(self, face: list) -> np.ndarray:
        """
        :param face:
        :return:
        """
        swapped_neighbours = self.swap_graph(face)

        neighbour_count = [len(node_neighbours) for node_neighbours in swapped_neighbours]
        degree_matrix = np.eye(self.nodeCount, dtype=np.int64) * np.array(neighbour_count)

        adjacency_matrix = np.zeros((self.nodeCount, self.nodeCount), dtype=np.int64)

        for node in range(self.nodeCount):
            adjacency_matrix[node, swapped_neighbours[node]] = 1

        laplacian_matrix = degree_matrix - adjacency_matrix

        return laplacian_matrix

    def swap_graph(self, face: list) -> list:
        """
        :param face:
        :return:
        """
        swapped_edges = deepcopy(self.Edges)

        for node_1, node_2 in enumerate(face):
            for edge in swapped_edges:
                if node_1 in edge and node_2 in edge:
                    continue
                elif node_1 in edge:
                    edge[edge.index(node_1)] = node_2
                elif node_2 in edge:
                    edge[edge.index(node_2)] = node_1

        swapped_neighbours = [[] for _ in range(self.nodeCount)]

        for node in range(self.nodeCount):
            for edge in swapped_edges:
                if node in edge:
                    swapped_neighbours[node].append(edge[not edge.index(node)])

        return swapped_neighbours

    def compute_remaining_representation(
            self, face: list, face_representation: np.ndarray, laplacian_matrix: np.ndarray
    ) -> np.ndarray:
        """
        :param face:
        :param face_representation:
        :param laplacian_matrix:
        :return:
        """
        face_length = len(face)
        matrix_b = laplacian_matrix[:face_length, face_length:]
        remaining_laplacian_matrix = laplacian_matrix[face_length:, face_length:]
        remaining_representation = (
                -face_representation @ matrix_b @ np.linalg.inv(remaining_laplacian_matrix)
        ).round(3)

        return remaining_representation

    def generate_random_remaining_representation(self, face: list, face_representation: np.ndarray) -> np.ndarray:
        """
        :param face:
        :param face_representation:
        :return:
        """
        face_length = len(face)
        random_coefficients = np.random.rand(face_length, self.nodeCount - face_length)
        random_coefficients = random_coefficients / np.sum(random_coefficients, axis=0)
        random_remaining_representation = (face_representation @ random_coefficients).round(3)

        return random_remaining_representation

    def save_representation(
            self, representation_file: str, random_representation_file: str, face: list,
            face_representation: np.ndarray, remaining_representation: np.ndarray,
            random_remaining_representation: np.ndarray
    ) -> None:
        """
        :param representation_file:
        :param random_representation_file:
        :param face:
        :param face_representation:
        :param remaining_representation:
        :param random_remaining_representation:
        :return: None
        """
        swapped_representation = np.append(face_representation, remaining_representation, axis=1)
        swapped_random_representation = np.append(face_representation, random_remaining_representation, axis=1)
        representation = np.transpose(self.swap_representation(face, swapped_representation))
        random_representation = np.transpose(self.swap_representation(face, swapped_random_representation))

        print(f"Saving coordinates to file: {representation_file}")

        assert (representation_file is not None)
        with open(representation_file, "w") as RepresentationFile:
            for coordinates in representation:
                RepresentationFile.write(f"{coordinates[0]} {coordinates[1]}\n")

        print(f"Saving random coordinates to file: {random_representation_file}")

        assert (random_representation_file is not None)
        with open(random_representation_file, "w") as RandomRepresentationFile:
            for coordinates in random_representation:
                RandomRepresentationFile.write(f"{coordinates[0]} {coordinates[1]}\n")

        print("Finished saving coordinates!")

    def swap_representation(self, face: list, swapped_representation: np.ndarray) -> np.ndarray:
        """
        :param face:
        :param swapped_representation:
        :return:
        """
        representation: np.ndarray = deepcopy(swapped_representation)

        for node_1, node_2 in zip(reversed(face), reversed(range(len(face)))):
            representation[:, [node_1, node_2]] = representation[:, [node_2, node_1]]

        return representation


if __name__ == "__main__":
    graph: Graph = Graph()
    if len(argv) == 2:
        print(f"Accepting arguments: {argv[1:]}")
        main_face = [int(x) for x in argv[1].split(',')]
        graph.main(main_face)
    else:
        graph.main()
