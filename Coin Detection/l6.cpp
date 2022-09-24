#include <bits/stdc++.h>
using namespace std;

class Point{
private:
    double x;
    double y;
    static bool sortY(Point a, Point b){
        return (b.y > a.y);
    };
    static bool sortX(Point a, Point b){
        return (b.x > a.x);
    };
public:
    Point(){
        x = double(rand())/RAND_MAX;
        y = double(rand())/RAND_MAX;
    }
    Point( double _x, double _y){
        x = _x;
        y = _y;
    }
    Point(const Point &other){
        x = other.x;
        y = other.y;
    }
    Point(Point &a, Point &b){
        x= (a.getX()+b.getX())/2;
        y = (a.getY()+b.getY())/2;
    }
    double getX(){
        return x;
    }
    double getY(){
        return y;
    }
    void scale(double factor){
        x*= factor;
        y*= factor;
    }
    static int orientation(Point &a, Point &b, Point &c){
        // 0 is colinear 1 is clockwise -1 is ccw
        double val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y);
        if(val == 0) return 0;
        return (val > 0)? 1:-1;
    }
    static double distance(Point &a, Point &b){
        return pow(pow(a.getY()-b.getY(),2)+pow(a.getX()-b.getX(),2),.5);
    }
    static double dist(double x1, double x2, double y1, double y2){
        return pow(pow(y2-y1,2)+pow(x2-x1,2),.5);
    }
    static double slope(Point &a, Point &b){
        return((b.y - a.y)/(b.x - a.x));
    }
    void print(){
        cout <<"(" << x << " , " << y << ") ";
    }
    bool equals(Point &other){
        return other.x - x < 0.000001 && other.y - y < 0.000001;
    }
    static vector<Point> sortWithY(vector<Point> points){
        sort(points.begin(),points.end(),sortY);
        return points;
    }
    static vector<Point> sortWithX(vector<Point> points){
        sort(points.begin(),points.end(),sortX);
        return points;
    }
};


class Line{
    double a;
    double b;
    double c;
    Point p;
    Point q;
    double m;
public:
    Line(){}
    Line(double _a, double _b, double _c){
        a = _a;
        b = _b;
        c = _c;
        m = -a/b;
        p = Point(0.0,c/b);
        q = Point(c/a,0.0);
    }
    Line(Point _p, double _m){
        p = _p;
        if(b != 0){
            m = -a/b;
            a = m;
            b = -1;
            c = (-p.getY() + m* p.getX());
        }
        else{
            m = numeric_limits<double>::infinity();
            a = 1;
            b = 0;
            c = p.getX();
        }
        a = m;
        b = -1;
        c = (-p.getY() + m* p.getX());
    }
    Line(double x1, double y1, double x2, double y2){
        Point _p(x1,y1);
        Point _q(x2,y2);
        p=_p;
        q=_q;
        if(_p.getX() - _q.getX() != 0){
            m = -a/b;
            a = _q.getY() - _p.getY();
            b = _p.getX() - _q.getX();
            c = a * _p.getX() + b * _p.getY();
        }
        else{
            m = numeric_limits<double>::infinity();
            a = 1;
            b = 0;
            c = p.getX();
        }
    }
    Line(Point& _p, Point& _q){
        p = _p;
        q = _q;
        if(_p.getX() - _q.getX() != 0){
            m = -a/b;
            a = _q.getY() - _p.getY();
            b = _p.getX() - _q.getX();
            c = a * _p.getX() + b * _p.getY();
        }
        else{
            m = numeric_limits<double>::infinity();
            a = 1;
            b = 0;
            c = p.getX();
        }
    }
    Line(const Line & other){
        a = other.a;
        b = other.b;
        c = other.c;
        p = other.p;
        m = other.m;
        q = other.q;
    }
    double getA(){
        return a;
    }
    double getB(){
        return b;
    }
    double getC(){
        return c;
    }
    double getM(){
        return m;
    }
    Point getP(){
        return p;
    }
    Point getQ(){
        return q;
    }
    Point getMidPoint(){
        Point m(p, q);
        return m;
    }
    double distance(){
        return Point::distance(p, q);
    }
    static Line min(Line &a, Line &b){
        if(a.distance() < b.distance()) return a;
        else return b;
    }
    double calcY(Point &c){
        if(m == numeric_limits<double>::infinity()){
            return p.getX();
        }
        return m*(c.getX() - p.getX())+p.getY();
    }
    void print(){
        //cout << "A: "<<a<< " B: "<<b<< " C: "<<c<<endl;
    }
    void printEnd(){
        //cout << "A: ";
        p.print();
        //cout << "B: ";
        q.print();
    }
    static Point intersection(Line &a, Line&b){
        if(a.m == numeric_limits<double>::infinity()){
            double x = a.getP().getX();
            Point n = a.getP();
            double y = b.calcY(n);
            Point ret(x,y);
            return ret;
        }
        if(b.m == numeric_limits<double>::infinity()){
            double x = b.getP().getX();
            Point n = b.getP();
            double y = a.calcY(n);
            Point ret(x,y);
            return ret;
        }
        double det = a.getA() * b.getB() - a.getB() * b.getA();
        double x = (b.getB() * a.getC() - a.getB() * b.getC())/det;
        double y = (a.getA() * b.getC() - b.getA() * a.getC())/det;
        Point p(x,y);
        return p;
    }
    static double distPointToLine(Line &l, Point &o){
        Line perp(o,-1/l.getM());
        Point intersect = Line::intersection(l, perp);
        double dist = Point::distance(o, intersect);
        return dist;
    }

};


class Circle{
    Point c;
    double r;
public:
    Circle(){}
    Circle(Point _c, double _r){
        c=  _c;
        r= _r;
    }
    Circle(int x, int y, int _r){
        c =  Point(x,y);
        r = _r;
    }
    Circle(const Circle &other){
        c = other.c;
        r = other.r;
    }
    Point getCenter(){
        return c;
    }
    double getRadius(){
        return r;
    }
    void scale(double factor){
        r*=factor;
        c.scale(factor);
    }
    void print(){
        cout <<"Radius: " << r << " Center: ";
        c.print();
        cout <<endl;
    }
};

class Pixel{
    int x;
    int y;
    int r;
    int g;
    int b;
public:
    Pixel(){}
    Pixel(int _x, int _y,int _r, int _g, int _b){
        x = _x;
        y = _y;
        r = _r;
        g = _g;
        b = _b;
    }
    void setColor(int _r, int _g, int _b){
        r = _r;
        g = _g;
        b = _b;
    }
    void toPPM(ofstream & out){
        out << r << " " << g << " " << b << " ";
    }
};

class Canvas{
    int** canvas;
    int size;
    int height,width;
    Pixel** image;
public:
    Canvas(int _size){
        size = _size;
        canvas = new int*[size];
        for(int i =0; i < size; i++){
            canvas[i] = new int[size];
        }
        clear();
    }
    Canvas(string name){ //read from file
        ifstream pixels(name);
        string r,g,b;
        getline(pixels,r); //reads p3
        getline(pixels,g,' '); //reads width
        width = stoi(g);
        int row=0,col=0;
        getline(pixels,b); //reads height
        height = stoi(b);
        cout <<width<< "(width, height) " << height <<endl;

        getline(pixels,b);  //reads the max value
        int** greyScale;
        greyScale = new int*[height];
        for(int i =0; i < height; i++){
            greyScale[i] = new int[width];
        }
        while(pixels >> r >> g >> b){
            int greyPixel = (stoi(r)+stoi(g)+stoi(b))/3;
            greyScale[row][col] = greyPixel;
            col++;
            if(col==width){
                row++;
                col=0;
            }
        }
        canvas = greyScale;
        size = max(width,height);
    }
    Canvas(int h, int w){
        size = max(h,w);
        canvas = new int*[h];
        for(int i =0; i < size; i++){
            canvas[i] = new int[w];
        }
        height = h;
        width = w;
        clear();
    }
    Canvas(string name, bool color){
        ifstream pixels(name);
        string r,g,b;
        getline(pixels,r); //reads p3
        getline(pixels,g,' '); //reads width
        width = stoi(g);
        int row=0,col=0;
        getline(pixels,b); //reads height
        height = stoi(b);
        cout << "width: "<< width <<" height: " << height <<endl;

        getline(pixels,b);  //reads the max value
        Pixel** img;
        img = new Pixel*[height];
        for(int i =0; i < height; i++){
            img[i] = new Pixel[width];
        }
        while(pixels >> r >> g >> b){
            Pixel p(col, row, stoi(r), stoi(g), stoi(b));
            img[row][col] = p;
            col++;
            if(col==width){
                row++;
                col=0;
            }
        }
        image = img;
        size = max(width,height);
    }
    int getHeight(){
        return height;
    }
    int getWidth(){
        return width;
    }
    int** getCanvas(){
        return canvas;
    }
    Pixel** getImage(){
        return image;
    }
    void clear(){
        for(int y = 0; y < height; y++){
            for(int x = 0; x < width; x++){
                canvas[y][x] = 1;
            }
        }
    }
    void drawImg(Circle &c, int r, int g, int b){
        if(c.getCenter().getX() <1 && c.getCenter().getY() < 1){
            c.scale(size);
        }
        int x, y, xmax, y2, y2_new, ty;
        xmax = (int) (c.getRadius() * 0.70710678 +.5);
        int xc = (int) (c.getCenter().getX() +.5);
        int yc = (int) (c.getCenter().getY() +.5);
        y = c.getRadius();
        y2 = y * y;
        ty = (2 * y) - 1; y2_new = y2;
        if(c.getRadius() > 3) xmax++;
        for (x = 0; x <= xmax; x++) {
            if ((y2 - y2_new) >= ty) {
                y2 -= ty;
                y -= 1;
                ty -= 2;
            }
            if(yc+y <height && yc+y >=0 && xc+x < width && xc+x >= 0) image[yc+y][xc+x].setColor(r, g, b);
            if(yc+y <height && yc+y >=0 && xc-x < width && xc-x >= 0) image[yc+y][xc-x].setColor(r, g, b);
            if(yc-y <height && yc-y >=0 && xc+x < width && xc+x >= 0) image[yc-y][xc+x].setColor(r, g, b);
            if(yc-y <height && yc-y >=0 && xc-x < width && xc+x >= 0) image[yc-y][xc-x].setColor(r, g, b);
            if(yc+x <height && yc+x >=0 && xc+y < width && xc+y >= 0) image[yc+x][xc+y].setColor(r, g, b);
            if(yc-x <height && yc-x >=0 && xc+y < width && xc+y >= 0) image[yc-x][xc+y].setColor(r, g, b);
            if(yc+x <height && yc+x >=0 && xc-y < width && xc-y >= 0) image[yc+x][xc-y].setColor(r, g, b);
            if(yc-x <height && yc-x >=0 && xc-y < width && xc-y >= 0) image[yc-x][xc-y].setColor(r, g, b);
            y2_new -= (2 * x) - 3;
        }
    }
    void draw(Point &a,int color){
        if(a.getX() < 1 && a.getY() < 1) {
            a.scale(size);
        }
        Circle c(a,3);
        draw(c,color);
    }
    void draw(Circle &c,int color){
        if(c.getCenter().getX() <1 && c.getCenter().getY() < 1){
            c.scale(size);
        }
        int x, y, xmax, y2, y2_new, ty;
        xmax = (int) (c.getRadius() * 0.70710678 +.5);
        int xc = (int) (c.getCenter().getX() +.5);
        int yc = (int) (c.getCenter().getY() +.5);
        y = c.getRadius();
        y2 = y * y;
        ty = (2 * y) - 1; y2_new = y2;
        if(c.getRadius() > 3) xmax++;
        for (x = 0; x <= xmax; x++) {
            if ((y2 - y2_new) >= ty) {
                y2 -= ty;
                y -= 1;
                ty -= 2;
            }
            if(yc+y <height && yc+y >=0 && xc+x < width && xc+x >= 0) canvas[yc+y][xc+x] = color;
            if(yc-y <height && yc-y >=0 && xc+x < width && xc+x >= 0) canvas[yc-y][xc+x] = color;
            if(yc+y <height && yc+y >=0 && xc-x < width && xc-x >= 0) canvas[yc+y][xc-x] = color;
            if(yc-y <height && yc-y >=0 && xc-x < width && xc+x >= 0) canvas[yc-y][xc-x] = color;
            if(yc+x <height && yc+x >=0 && xc+y < width && xc+y >= 0) canvas[yc+x][xc+y] = color;
            if(yc-x <height && yc-x >=0 && xc+y < width && xc+y >= 0) canvas[yc-x][xc+y] = color;
            if(yc+x <height && yc+x >=0 && xc-y < width && xc-y >= 0) canvas[yc+x][xc-y] = color;
            if(yc-x <height && yc-x >=0 && xc-y < width && xc-y >= 0) canvas[yc-x][xc-y] = color;
            y2_new -= (2 * x) - 3;
        }
    }
    void draw(Point &a, Point &b, int color){
        if(a.getX() <1 && a.getY() < 1){
            a.scale(size);
        }
        if(b.getX() <1 && b.getY() < 1){
            b.scale(size);
        }
        int x1 =  (int) (a.getX() +.5);
        int x2 =  (int) (b.getX() +.5);
        int y1 =  (int) (a.getY() +.5);
        int y2 =  (int) (b.getY() +.5);
        int w = x2 - x1 ;
        int h = y2 - y1 ;
        int dx1 = 0, dy1 = 0, dx2 = 0, dy2 = 0 ;
        if (w<0) dx1 = -1 ; else if (w>0) dx1 = 1 ;
        if (h<0) dy1 = -1 ; else if (h>0) dy1 = 1 ;
        if (w<0) dx2 = -1 ; else if (w>0) dx2 = 1 ;
        int longest = abs(w);
        int shortest = abs(h);
        if (longest <= shortest) {
            longest = abs(h);
            shortest = abs(w);
            if (h<0) dy2 = -1 ; else if (h>0) dy2 = 1 ;
            dx2 = 0 ;
        }
        int numerator = 1;
        for (int i=0;i<=longest;i++) {
            if(y1 <height && y1 >=0 && x1 < width && x1 >= 0) canvas[y1][x1] = color;
            numerator += shortest ;
            if (numerator >= longest) {
                numerator -= longest ;
                x1 += dx1 ;
                y1 += dy1 ;
            } else {
                x1 += dx2 ;
                y1 += dy2 ;
            }
        }
    }
    void draw(Line &l, int color){
        Point a = l.getP();
        double dx = size+1-a.getX();
        double dy = size+1-a.getY()*l.getM();
        Point b;
        while(a.getX() < size && a.getX() >=0 && a.getY() < size && a.getY() >= 0){
            b = Point(a.getX()+dx, a.getY()+dy);
            draw(a,b,color);
            a = b;
        }
        a = l.getP();
        while(a.getX() <size && a.getX() >=0 && a.getY() < size && a.getY() >= 0){
            b= Point(a.getX()-dx, a.getY()-dy);
            draw(a,b, color);
            a = b;
        }
    }
    void canny(int threshold){
        int sobel_x[3][3] = { {-1,0,1},{-2,0,2},{-1,0,1}};
        int sobel_y[3][3] = { {1,2,1},{0,0,0},{-1,-2,-1}};
        int** sobel_image;
        sobel_image = new int*[height];
        for(int i =0; i < height; i++){
            sobel_image[i] = new int[width];
        }
        for(int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                if(x == 0 || y == 0 || x == width-1 || y == height -1)
                    sobel_image[y][x] = 0;
                else{
                    int gx=0,gy=0;
                    for(int r = -1;r <2;r++){
                        for(int c = -1;c<2;c++){
                            gx+=canvas[y+r][x+c]*sobel_x[1+r][1+c];
                            gy+=canvas[y+r][x+c]*sobel_y[1+r][1+c];
                        }
                    }
                    int magnitude = (int) pow(pow(gx,2) + pow(gy,2),.5);
                    sobel_image[y][x] = magnitude;
                    sobel_image[y][x] = 0;
                    if(magnitude > threshold)
                        sobel_image[y][x] = 1;
                }
            }
        }
        canvas = sobel_image;
    }
    int** sobel_magnitude(){
        int sobel_x[3][3] = { {-1,0,1},{-2,0,2},{-1,0,1}};
        int sobel_y[3][3] = { {1,2,1},{0,0,0},{-1,-2,-1}};
        int** sobel_mag = new int*[height];
        for(int i =0; i < height; i++){
            sobel_mag[i] = new int[width];
        }
        for(int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                if(x == 0 || y == 0 || x == width-1 || y == height -1)
                    sobel_mag[y][x] = 0;

                else{
                    int gx=0,gy=0;
                    for(int r = -1;r <2;r++){
                        for(int c = -1;c<2;c++){
                            gx+=canvas[y+r][x+c]*sobel_x[1+r][1+c];
                            gy+=canvas[y+r][x+c]*sobel_y[1+r][1+c];
                        }
                    }
                    int magnitude = (int) pow(pow(gx,2) + pow(gy,2),.5);
                    sobel_mag[y][x] = magnitude;
                }
            }
        }
        return sobel_mag;
    }
    double** sobel_angle(){
        int sobel_x[3][3] = { {-1,0,1},{-2,0,2},{-1,0,1}};
        int sobel_y[3][3] = { {1,2,1},{0,0,0},{-1,-2,-1}};
        double** sobel_dir = new double*[height];
        for(int i =0; i < height; i++){
            sobel_dir[i] = new double[width];
        }
        for(int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                if(x == 0 || y == 0 || x == width-1 || y == height -1)
                    sobel_dir[y][x] = 0;
                else{
                    double gx=0,gy=0;
                    for(int r = -1;r <2;r++){
                        for(int c = -1;c<2;c++){
                            gx+=canvas[y+r][x+c]*sobel_x[1+r][1+c];
                            gy+=canvas[y+r][x+c]*sobel_y[1+r][1+c];
                        }
                    }
                    double dir;
                    if(gx == 0)
                        dir = 90;
                    else if(gy == 0)
                        dir = 0;
                    else
                        dir = gy/gx;
                    sobel_dir[y][x] = dir;
                }
            }
        }
        return sobel_dir;
    }
    double** voting_dir(){
        int sobel_x[3][3] = { {-1,0,1},{-2,0,2},{-1,0,1}};
        int sobel_y[3][3] = { {1,2,1},{0,0,0},{-1,-2,-1}};
        double** sobel_dir = new double*[height];
        for(int i =0; i < height; i++){
            sobel_dir[i] = new double[width];
        }
        for(int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                if(x == 0 || y == 0 || x == width-1 || y == height -1)
                    sobel_dir[y][x] = 0;
                else{
                    double gx=0,gy=0;
                    for(int r = -1;r <2;r++){
                        for(int c = -1;c<2;c++){
                            gx+=canvas[y+r][x+c]*sobel_x[1+r][1+c];
                            gy+=canvas[y+r][x+c]*sobel_y[1+r][1+c];
                        }
                    }
                    double dir;
                    if(gx == 0)
                        dir = numeric_limits<double>::infinity();
                    else if(gy == 0)
                        dir = 0;
                    else
                        dir = -gy/gx;
                    sobel_dir[y][x] = dir;
                }
            }
        }
        return sobel_dir;
    }
    void nonMaximalSupression(double** sobel_dir, int** sobel_mag){
        for(int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                double angle = atan(sobel_dir[y][x]);
                if( angle < -67.5){ //-90
                    if( sobel_mag[y][x] > sobel_mag[y-1][x] && sobel_mag[y][x] > sobel_mag[y+1][x] )
                        canvas[y][x] = 1;
                    else
                        canvas[y][x] = 0;
                }
                else if( angle < -22.5){ //-45
                    if( sobel_mag[y][x] > sobel_mag[y-1][x-1] && sobel_mag[y][x] > sobel_mag[y+1][x+1] )
                        canvas[y][x] = 1;
                    else
                        canvas[y][x] = 0;
                }
                else if( angle < 22.5){ // 0
                    if( sobel_mag[y][x] > sobel_mag[y][x-1] && sobel_mag[y][x] > sobel_mag[y][x+1] )
                        canvas[y][x] = 1;
                    else
                        canvas[y][x] = 0;
                }
                else if( angle < 67.5){ //45
                    if( sobel_mag[y][x] > sobel_mag[y+1][x-1] && sobel_mag[y][x] > sobel_mag[y-1][x+1] )
                        canvas[y][x] = 1;
                    else
                        canvas[y][x] = 0;
                }
                else{// 90
                    if( sobel_mag[y][x] > sobel_mag[y+1][x] && sobel_mag[y][x] > sobel_mag[y-1][x] )
                        canvas[y][x] = 1;
                    else
                        canvas[y][x] = 0;
                }

            }
        }

    }
    void doubleThreshold(int t1, int t2, int** sobel_mag){
        vector<pair<int,int>> threes;
        for(int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                if(sobel_mag[y][x] < t1){
                    canvas[y][x] =0;
                }
                else if(sobel_mag[y][x] < t2)
                    canvas[y][x] = 2;
                else{
                    canvas[y][x] = 3;
                    threes.push_back(make_pair(y,x));
                }
                //cout << canvas[y][x] << " ";
            }
            //cout << endl;
        }
        for(int i = 0; i < threes.size(); i++){
            dtRecursive(threes.at(i));
        }

    }
    void dtRecursive(pair<int,int> index){
        int x = index.second;
        int y = index.first;
        //cout << canvas[y][x];
        canvas[y][x] = 1;
        if(x > 0 && canvas[y][x] == 2)
            dtRecursive(make_pair(y,x-1));
        if(x +1 < size && canvas[y][x] == 2)
            dtRecursive(make_pair(y,x+1));
        if(y > 0 && canvas[y][x] == 2)
            dtRecursive(make_pair(y-1,x));
        if(y +1 < size && canvas[y][x] == 2)
            dtRecursive(make_pair(y+1,x));

    }
    void makePPM(string name,int range){
        ofstream img(name);
        img << "P3 ";
        img << width << " " << height << " ";
        img << range << endl;
        for(int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                img << canvas[y][x] << " " << canvas[y][x] << " " << canvas[y][x] <<" ";
            }
            img << "\n";
        }
    }
    void makeColorPPM(string name){
        ofstream img(name);
        img << "P3 ";
        img << width << " " << height << " ";
        img << 255 << endl;
        for(int r = 0; r < height; r++){
            for(int c = 0; c < width; c++){
                image[r][c].toPPM(img);
            }
        }
    }
    void bresenheimVote(int*** votes,int startx, int starty, double angle, int dir, int r_max){
        int x1 = startx;
        int x2 = (int) (dir*(startx + r_max)) ;
        int y1 = starty;
        int y2 = y1;
        if(isinf(angle) == false)
            y2 = (int) (dir*(y1 + angle * r_max));
        int w = x2 - x1 ;
        int h = y2 - y1 ;
        //cout << "width: " << w << " height: " << h << " angle: "<< angle <<endl;
        int dx1 = 0, dy1 = 0, dx2 = 0, dy2 = 0 ;
        if (w<0) dx1 = -1 ; else if (w>0) dx1 = 1 ;
        if (h<0) dy1 = -1 ; else if (h>0) dy1 = 1 ;
        if (w<0) dx2 = -1 ; else if (w>0) dx2 = 1 ;
        int longest = abs(w);
        int shortest = abs(h);
        if (longest <= shortest) {
            longest = abs(h);
            shortest = abs(w);
            if (h<0) dy2 = -1 ; else if (h>0) dy2 = 1 ;
            dx2 = 0 ;
        }
        int numerator = 1;
        int dist = 0;
        for (int i=0;i<=longest;i++) {
            if(y1 <height && y1 >=0 && x1 < width && x1 >= 0 && dist < r_max && dist >=0) votes[y1][x1][dist] += 1;
            numerator += shortest;
            if (numerator >= longest) {
                numerator -= longest ;
                x1 += dx1 ;
                y1 += dy1 ;
                dist += dx1 +dy1;
            } else {
                x1 += dx2 ;
                y1 += dy2 ;
                dist += dx2 +dy2;
            }
        }
    }
    int** gaussian_blur(int** img){
        int kernel[5][5] = {{1,4,7,4,1},{4,16,26,16,4},{7,26,41,26,7},{4,16,26,16,4},{1,4,7,4,1}};
        int** blurred = new int*[height];
        for(int i =0; i < height; i++){
            blurred[i] = new int[width];
        }
        for(int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                if(x < 2 || y < 2 || x >= width -2 || y >= height -2)
                    blurred[y][x] = 0;
                else{
                    blurred[y][x] = 0;
                    for(int r = -2;r <2;r++){
                        for(int c = -2;c<2;c++){
                            blurred[y][x]+=img[y+r][x+c]*kernel[2+r][2+c];
                        }
                    }
                    blurred[y][x] /= 273;
                }
            }
        }
        return blurred;
    }
    int** findCircles(double** sobel_dir){//returns matrix where r = circle center with radius r and 0 means no circle
        int r_max = 60;
        int r_min = 20;
        int threshold = 4;
        int*** votes = new int**[height];
        for(int i =0; i < height; i++){
            votes[i] = new int*[width];
            for(int j =0; j < width; j++){
                votes[i][j] = new int[r_max];
                for(int k=0; k< r_max ;k++){
                    votes[i][j][k] =0;
                }
            }
        }
        cout << "created 3d matrix\n";
        for(int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                if(canvas[y][x] == 1){
                    bresenheimVote(votes,x,y,-sobel_dir[y][x],1, r_max);
                    bresenheimVote(votes,x,y,-sobel_dir[y][x],-1, r_max);
                }
            }
        }
        cout <<"voting done\n";
        int** centers = new int*[height];
        for(int y =0; y< height; y++){
            centers[y] = new int[width];
        }
        cout << "created 2d matrix\n";
        for(int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int mode_radius = r_min;
                int mode_count = 0;
                for(int r =r_min; r < r_max-2; r++){
                    if(votes[y][x][r] + votes[y][x][r-1] + votes[y][x][r+1] + votes[y][x][r-2] + votes[y][x][r+2]  > mode_count){
                        mode_radius = r;
                        mode_count = votes[y][x][r] + votes[y][x][r-1] + votes[y][x][r+1] + votes[y][x][r-2] + votes[y][x][r+2];
                        //cout << mode_count << " ";
                    }
                }
                //cout << mode_radius << " ";
                if( votes[y][x][mode_radius-1] + votes[y][x][mode_radius] + votes[y][x][mode_radius+1] + votes[y][x][mode_radius-2] + votes[y][x][mode_radius+2] > threshold){
                    centers[y][x] = mode_radius;

                }
                else
                    centers[y][x] = -1;


            }
        }
        for(int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                if(centers[y][x] > 0){
                    for(int dy = -30; dy < 40; dy++){ // find local max
                        for(int dx = -30; dx < 40; dx++){
                            if(y+dy < height && y+dy >=0 && x+dx >=0 && x+dx <width && centers[y+dy][x+dx] >0){
                                if( centers[y][x] > centers[y+dy][x+dx] && votes[y][x][centers[y][x]] >= votes[y+dy][x+dx][centers[y+dy][x+dx]]){
                                    centers[y][x] += centers[y+dy][x+dx];
                                    centers[y+dy][x+dx] = -1;
                                    centers[y][x] = (int) (9*centers[y][x]/20);
                                    votes[y][x][centers[y][x]] +=votes[y+dy][x+dx][centers[y+dy][x+dx]];                                }
                            }
                        }
                    }
                }
            }
        }
        cout <<"local cluster flitering completed \n";
        for(int i =0; i < height; i++){
            for(int j =0; j < width; j++){
                delete[] votes[i][j];
            }
            delete[] votes[i];
        }
        delete[] votes;
        return centers;
    }
    bool checkCircleValidity(Circle& c, int** edges){
        double threshold= .12;
        int alligned = 0;
        double total = 0.0;
        int x, y, xmax, y2, y2_new, ty;
        xmax = (int) (c.getRadius() * 0.70710678 +.5);
        int xc = (int) (c.getCenter().getX() +.5);
        int yc = (int) (c.getCenter().getY() +.5);
        y = c.getRadius();
        y2 = y * y;
        ty = (2 * y) - 1; y2_new = y2;
        for (x = 0; x <= xmax; x++) {
            if ((y2 - y2_new) >= ty) {
                y2 -= ty;
                y -= 1;
                ty -= 2;
            }
            if(yc+y <height && yc+y >=0 && xc+x < width && xc+x >= 0 && edges[yc+y][xc+x] == 1)  alligned += 1;
            if(yc-y <height && yc-y >=0 && xc+x < width && xc+x >= 0 && edges[yc-y][xc+x] == 1)  alligned += 1;
            if(yc+y <height && yc+y >=0 && xc-x < width && xc-x >= 0 && edges[yc+y][xc-x] == 1)  alligned += 1;
            if(yc-y <height && yc-y >=0 && xc-x < width && xc+x >= 0 && edges[yc-y][xc-x] == 1)  alligned += 1;
            if(yc+x <height && yc+x >=0 && xc+y < width && xc+y >= 0 && edges[yc+x][xc+y] == 1)  alligned += 1;
            if(yc-x <height && yc-x >=0 && xc+y < width && xc+y >= 0 && edges[yc-x][xc+y] == 1)  alligned += 1;
            if(yc+x <height && yc+x >=0 && xc-y < width && xc-y >= 0 && edges[yc+x][xc-y] == 1)  alligned += 1;
            if(yc-x <height && yc-x >=0 && xc-y < width && xc-y >= 0 && edges[yc-x][xc-y] == 1)  alligned += 1;
            total+=8;
            y2_new -= (2 * x) - 3;
        }
        return (alligned/total > threshold);

    }
    //to do:  draw circles based on the circle centers. Then remove circles that don't really align with edges (count the ratio that intersects the edge matrix)
    // make a vector of radii and bin them into penny nickel dime quarter size and caclulate value
};


int main() {
    string name = "coinsMedium.ppm";
    Canvas nms(name); cout <<"loaded image \n";
    double** sobel_dir = nms.sobel_angle();
    int** sobel_mag = nms.sobel_magnitude();
    nms.nonMaximalSupression(sobel_dir, sobel_mag); cout <<"performed nonMaximalSupression \n";
    Canvas edges(name);
    edges.doubleThreshold(60, 200, sobel_mag);cout <<"performed double threshold \n";

    for(int i =0; i < nms.getHeight(); ++i){
        delete[] sobel_mag[i];
    }
    delete[] sobel_mag;

    int height = nms.getHeight();
    int width = nms.getWidth();

    for(int r = 0; r < height; r++){
        for(int c = 0; c < width; c++){
            if(nms.getCanvas()[r][c] == 1 && edges.getCanvas()[r][c] == 1){
                edges.getCanvas()[r][c] = 1;
            }
            else
                edges.getCanvas()[r][c] = 0;
        }
    }
    edges.makePPM("imagef.ppm",1); cout << "made canny ppm \n";
    for(int i =0; i < nms.getHeight(); ++i){
        delete[] nms.getCanvas()[i];
    }
    delete[] nms.getCanvas();

    int** circles = edges.findCircles(sobel_dir);
    for(int i =0; i < height; ++i){
        delete[] sobel_dir[i];
    }



    delete[] sobel_dir;
    string out = "imagec.ppm";
    string results = "results.txt";
    ofstream img(out);
    ofstream res(results);
    img << "P3 ";
    img << edges.getWidth() << " " << edges.getHeight() << " ";
    img << 255 << endl;
    int radii_dist[60];
    for(int i =0 ; i< 60; i++){
        radii_dist[i] = 0;
    }
    vector<Circle> good_circles;
    for(int y = 0; y < height; y++){
        for(int x=0; x < width; x++){
            if(circles[y][x] > 1){
                Circle c(x, y, circles[y][x]);
                Circle cd(x, y, circles[y][x]+1);
                Circle cde(x, y, circles[y][x]+2);
                radii_dist[circles[y][x]] +=1;
                good_circles.push_back(c);good_circles.push_back(cd);good_circles.push_back(cde);
            }

        }
    }

    Canvas detected_coins(name, true);
    cout <<good_circles.size() << endl;
    for(int i=0; i < good_circles.size(); ++i){
        //good_circles[i].print();
        detected_coins.drawImg(good_circles[i],255,0,0);
    }
    int num_penny=0, num_nickel=0, num_dime=0, num_quarter=0, num_half=0;
    for(int i =0 ; i< 60; i++){
        cout <<"circle radius distribution for "<< i << ": " <<radii_dist[i]<< "\n";
        if(i > 20 && i<= 25) num_penny += radii_dist[i];
        if(i <= 20) num_dime += radii_dist[i];
        if(i > 25 && i<=30) num_nickel += radii_dist[i];
        if(i > 30 && i<=40) num_quarter += radii_dist[i];
        if(i > 42) num_half += radii_dist[i];
    }
    res << "Number of pennies detected: " << num_penny <<endl;
    res << "Number of nickels detected: " << num_nickel <<endl;
    res << "Number of dimes detected: " << num_dime <<endl;
    res << "Number of quarters detected: " << num_quarter <<endl;
    res << "Number of half dollars detected: " << num_half <<endl;
    res << "Total value of coins: " << num_dime * 10 + num_half * 50 + num_penny + num_quarter * 25 + num_nickel * 5<< " cents";

    cout << "Number of pennies detected: " << num_penny <<endl;
    cout << "Number of nickels detected: " << num_nickel <<endl;
    cout << "Number of dimes detected: " << num_dime <<endl;
    cout << "Number of quarters detected: " << num_quarter <<endl;
    cout << "Number of half dollars detected: " << num_half <<endl;
    cout << "Total value of coins: " << (num_dime * 10 + num_half * 50 + num_penny + num_quarter * 25 + num_nickel * 5) << " cents\n";

    detected_coins.makeColorPPM(out);
    cout <<"done\n";
}
