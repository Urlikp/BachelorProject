#include <iostream>
#include <GL/glew.h>
#include <GL/freeglut.h>
#include <fstream>
#include <vector>
#include <cmath>

#define APP_NAME    "Algebraic Graph Theory"

#define RETURN_OK       0
#define RETURN_ERROR    1

#define GRAPH_FILE                  "input_graph.txt"
#define REPRESENTATION_FILE         "input_representation.txt"
#define RANDOM_REPRESENTATION_FILE  "input_random_representation.txt"

#define DIMENSION   2

#define RED         1.0f, 0.0f, 0.0f, 1.0f
#define GREEN       0.0f, 1.0f, 0.0f, 1.0f
#define BLUE        0.0f, 0.0f, 1.0f, 1.0f
#define BACKGROUND  0.0f, 0.0f, 0.0f, 0.0f

#define POINT_SIZE  15.0f
#define LINE_WIDTH  2.0f

#define WINDOW_SIZE     1280
#define WINDOW_POSITION 200

#define ESCAPE_KEY      27
#define ANIMATION_KEY   'f'

struct appState {
    float appElapsedTime = 0.0f;
    float animationStartTime = 0.0f;
    bool runAnimation = false;
} AppState;

struct graph {
    int nodeCount = 0;
    int edgeCount = 0;
    std::vector<int> Edges;
    std::vector<float> NodeCoordinates;
    std::vector<float> NodeRandomCoordinates;
    std::vector<float> NodeCorrectCoordinates;
} Graph;

void RenderScene() {
    glClear(GL_COLOR_BUFFER_BIT);

    int nodeIndex;

    glColor4f(GREEN);

    glBegin( GL_POINTS);
        for (int i = 0; i < Graph.nodeCount; i++) {
            nodeIndex = DIMENSION * i;
            glVertex2f(Graph.NodeCoordinates.at(nodeIndex), Graph.NodeCoordinates.at(nodeIndex + 1));
        }
    glEnd();

    glBegin( GL_LINES);
        for (int i = 0; i < Graph.edgeCount; i++) {
            nodeIndex = DIMENSION * Graph.Edges.at(DIMENSION * i);
            glVertex2f(Graph.NodeCoordinates.at(nodeIndex), Graph.NodeCoordinates.at(nodeIndex + 1));
            nodeIndex = DIMENSION * Graph.Edges.at((DIMENSION * i) + 1);
            glVertex2f(Graph.NodeCoordinates.at(nodeIndex), Graph.NodeCoordinates.at(nodeIndex + 1));
        }
    glEnd();

    glColor4f(RED);

    for (int i = 0; i < Graph.nodeCount; i++) {
        nodeIndex = DIMENSION * i;
        glRasterPos2f(Graph.NodeCoordinates.at(nodeIndex) + (2 * POINT_SIZE / WINDOW_SIZE),
                      Graph.NodeCoordinates.at(nodeIndex + 1) + (2 * POINT_SIZE / WINDOW_SIZE));

        std::string nodeIndexString = std::to_string(i);

        for (const char &nodeIndexChar : nodeIndexString) {
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, nodeIndexChar);
        }
    }

    glutSwapBuffers();
}

void KeyboardCallback(unsigned char keyPressed, int mouseX, int mouseY) {
    switch(keyPressed) {
        case ESCAPE_KEY:
            glutLeaveMainLoop();
            break;
        case ANIMATION_KEY:
            if (!AppState.runAnimation) {
                AppState.runAnimation = true;
                AppState.animationStartTime = AppState.appElapsedTime;
            }

            break;
        default:
            break;
    }
}

float LinearInterpolation(int nodeIndex, float speed) {
    float currentCoordinate =
            (1 - speed) * Graph.NodeRandomCoordinates.at(nodeIndex)
            + speed * Graph.NodeCorrectCoordinates.at(nodeIndex);

    return currentCoordinate;
}

void TimerCallback(int) {
    AppState.appElapsedTime = 0.002f * (float)glutGet(GLUT_ELAPSED_TIME);

    if (AppState.runAnimation) {
        int nodeIndex;
        float timeParameter = AppState.appElapsedTime - AppState.animationStartTime;
        float exponential = exp(timeParameter - 6);
        float speed = exponential / (exponential + 1);

        std::cout << speed << std::endl;

        if (timeParameter > 12) {
            return;
        }

        for (int i = 0; i < Graph.nodeCount; i++) {
            nodeIndex = DIMENSION * i;
            Graph.NodeCoordinates.at(nodeIndex) = LinearInterpolation(nodeIndex, speed);
            Graph.NodeCoordinates.at(nodeIndex + 1) = LinearInterpolation(nodeIndex + 1, speed);
        }
    }

    glutTimerFunc(33, TimerCallback, 0);

    glutPostRedisplay();
}

void OpenGLSetup() {
    glClearColor(BACKGROUND);
    glPointSize(POINT_SIZE);
    glLineWidth(LINE_WIDTH);

    glutDisplayFunc(RenderScene);
    glutKeyboardFunc(KeyboardCallback);
    glutTimerFunc(33, TimerCallback, 0);
}

int OpenGLInit(int* argc, char** argv) {
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
    std::ifstream RandomRepresentationFile(RANDOM_REPRESENTATION_FILE);

    if (!GraphFile.is_open() || !RepresentationFile.is_open() || !RandomRepresentationFile.is_open()) {
        std::cerr << "Error: files could not be opened" << std::endl;
        std::cerr << GRAPH_FILE << ": " << GraphFile.is_open() << std::endl;
        std::cerr << REPRESENTATION_FILE << ": " << RepresentationFile.is_open() << std::endl;
        std::cerr << RANDOM_REPRESENTATION_FILE << ": " << RandomRepresentationFile.is_open() << std::endl;
        return RETURN_ERROR;
    }

    GraphFile >> Graph.nodeCount;

    Graph.NodeCoordinates.reserve(DIMENSION * Graph.nodeCount);
    Graph.NodeCorrectCoordinates.reserve(DIMENSION * Graph.nodeCount);
    Graph.NodeRandomCoordinates.reserve(DIMENSION * Graph.nodeCount);

    int edgeBegin, edgeEnd;

    while (!GraphFile.eof()) {
        GraphFile >> edgeBegin >> edgeEnd;

        Graph.Edges.push_back(edgeBegin);
        Graph.Edges.push_back(edgeEnd);
        Graph.edgeCount++;
    }

    float nodeX, nodeY;

    while (!RepresentationFile.eof()) {
        RepresentationFile >> nodeX >> nodeY;

        Graph.NodeCorrectCoordinates.push_back(nodeX);
        Graph.NodeCorrectCoordinates.push_back(nodeY);
    }

    while (!RandomRepresentationFile.eof()) {
        RandomRepresentationFile >> nodeX >> nodeY;

        Graph.NodeCoordinates.push_back(nodeX);
        Graph.NodeRandomCoordinates.push_back(nodeX);
        Graph.NodeCoordinates.push_back(nodeY);
        Graph.NodeRandomCoordinates.push_back(nodeY);
    }

    GraphFile.close();
    RepresentationFile.close();
    RandomRepresentationFile.close();

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
