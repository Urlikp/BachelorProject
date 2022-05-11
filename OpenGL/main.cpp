#include <iostream>
#include <GL/glew.h>
#include <GL/freeglut.h>
#include <fstream>
#include <vector>

#define APP_NAME    "Algebraic Graph Theory"

#define RETURN_OK       0
#define RETURN_ERROR    1

#define GRAPH_FILE          "input_graph.txt"
#define REPRESENTATION_FILE "input_representation.txt"

#define DIMENSION   2

#define RED         1.0f, 0.0f, 0.0f, 1.0f
#define GREEN       0.0f, 1.0f, 0.0f, 1.0f
#define BLUE        0.0f, 0.0f, 1.0f, 1.0f
#define BACKGROUND  0.0f, 0.0f, 0.0f, 0.0f

#define POINT_SIZE  15.0f
#define LINE_WIDTH  2.0f

#define WINDOW_SIZE     1280
#define WINDOW_POSITION 200

int nodeCount, edgeCount;
std::vector<int> Edges;
std::vector<float> NodeCoordinates;

void RenderScene() {
    glClear(GL_COLOR_BUFFER_BIT);

    int nodeIndex;

    glColor4f(GREEN);

    glBegin( GL_POINTS);
        for (int i = 0; i < nodeCount; i++) {
            nodeIndex = DIMENSION * i;
            glVertex2f(NodeCoordinates.at(DIMENSION * i), NodeCoordinates.at((DIMENSION * i) + 1));
        }
    glEnd();

    glBegin( GL_LINES);
        for (int i = 0; i < edgeCount; i++) {
            nodeIndex = DIMENSION * Edges.at(DIMENSION * i);
            glVertex2f(NodeCoordinates.at(nodeIndex), NodeCoordinates.at(nodeIndex + 1));
            nodeIndex = DIMENSION * Edges.at((DIMENSION * i) + 1);
            glVertex2f(NodeCoordinates.at(nodeIndex), NodeCoordinates.at(nodeIndex + 1));
        }
    glEnd();

    glColor4f(RED);

    for (int i = 0; i < nodeCount; i++) {
        nodeIndex = DIMENSION * i;
        glRasterPos2f(NodeCoordinates.at(DIMENSION * i) + (2 * POINT_SIZE / WINDOW_SIZE), NodeCoordinates.at((DIMENSION * i) + 1) + (2 * POINT_SIZE / WINDOW_SIZE));

        std::string nodeIndexString = std::to_string(i);

        for (const char &nodeIndexChar : nodeIndexString) {
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, nodeIndexChar);
        }
    }

    glutSwapBuffers();
}

void OpenGLSetup() {
    glClearColor(BACKGROUND);
    glPointSize(POINT_SIZE);
    glLineWidth(LINE_WIDTH);

    glutDisplayFunc(RenderScene);
}

int OpenGLInit(int *argc, char** argv) {
    glutInit(argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA);

    glutInitWindowSize(WINDOW_SIZE, WINDOW_SIZE);
    glutInitWindowPosition(WINDOW_POSITION, WINDOW_POSITION);

    int window = glutCreateWindow(APP_NAME);
    std::cout << "Window ID: " << window << std::endl;

    GLenum res = glewInit();
    if (res != GLEW_OK) {
        std::cerr << "Error: " << glewGetErrorString(res) << std::endl;
        return RETURN_ERROR;
    }

    return RETURN_OK;
}

int LoadInput() {
    std::ifstream GraphFile(GRAPH_FILE);
    std::ifstream RepresentationFile(REPRESENTATION_FILE);

    if (!GraphFile.is_open() || !RepresentationFile.is_open()) {
        std::cerr << "Error: files could not be opened" << std::endl;
        std::cerr << GRAPH_FILE << ": " << GraphFile.is_open() << std::endl;
        std::cerr << REPRESENTATION_FILE << ": " << RepresentationFile.is_open() << std::endl;
        return RETURN_ERROR;
    }

    GraphFile >> nodeCount;
    edgeCount = 0;
    NodeCoordinates.reserve(DIMENSION * nodeCount);

    int edgeBegin, edgeEnd;

    while (!GraphFile.eof()) {
        GraphFile >> edgeBegin >> edgeEnd;
        Edges.push_back(edgeBegin);
        Edges.push_back(edgeEnd);
        edgeCount++;
    }

    float nodeX, nodeY;

    while (!RepresentationFile.eof()) {
        RepresentationFile >> nodeX >> nodeY;
        NodeCoordinates.push_back(nodeX);
        NodeCoordinates.push_back(nodeY);
    }

    GraphFile.close();
    RepresentationFile.close();

    return RETURN_OK;
}

int main(int argc, char** argv) {
    std::cout << "Hello, Algebraic Graph Theory!" << std::endl;

    if (LoadInput() == RETURN_ERROR) {
        return RETURN_ERROR;
    }

    if (OpenGLInit(&argc, argv) == RETURN_ERROR) {
        return RETURN_ERROR;
    }

    OpenGLSetup();

    glutMainLoop();

    return RETURN_OK;
}
