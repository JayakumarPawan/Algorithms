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
    // 0 is colinear 1 is clockwise -1 is ccw
    static int orientation(Point &a, Point &b, Point &c){
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
        //cout <<"Radius: " << r << " Center: ";
        c.print();
    }
};
class Canvas{
    int** canvas;
    int size;
    int height,width;
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
        size = width;
    }
    Canvas(int h, int w){
        size = h;
        canvas = new int*[h];
        for(int i =0; i < size; i++){
            canvas[i] = new int[w];
        }
        height = h;
        width = w;
        clear();
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
    void clear(){
        for(int y = 0; y < size; y++){
            for(int x = 0; x < size; x++){
                canvas[y][x] = 1;
            }
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
            if(yc+y <size && yc+y >=0 && xc+x < size && xc+x >= 0) canvas[yc+y][xc+x] = color;
            if(yc-y <size && yc-y >=0 && xc+x < size && xc+x >= 0) canvas[yc-y][xc+x] = color;
            if(yc+y <size && yc+y >=0 && xc-x < size && xc-x >= 0) canvas[yc+y][xc-x] = color;
            if(yc-y <size && yc-y >=0 && xc-x < size && xc+x >= 0) canvas[yc-y][xc-x] = color;
            if(yc+x <size && yc+x >=0 && xc+y < size && xc+y >= 0) canvas[yc+x][xc+y] = color;
            if(yc-x <size && yc-x >=0 && xc+y < size && xc+y >= 0) canvas[yc-x][xc+y] = color;
            if(yc+x <size && yc+x >=0 && xc-y < size && xc-y >= 0) canvas[yc+x][xc-y] = color;
            if(yc-x <size && yc-x >=0 && xc-y < size && xc-y >= 0) canvas[yc-x][xc-y] = color;
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
            if(y1 <size && y1 >=0 && x1 < size && x1 >= 0) canvas[y1][x1] = color;
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
                    int gx=0,gy=0;
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
                        dir = atan(gy/gx);
                    sobel_dir[y][x] = dir;
                }
            }
        }
        return sobel_dir;
    }
    void nonMaximalSupression(){
        int** sobel_mag = sobel_magnitude();
        cout << "created sobel magnitudes\n";
        double** sobel_dir = sobel_angle();
        cout << "created sobel angles\n";
        for(int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                if( sobel_dir[y][x] < -67.5){ //-90
                    if( sobel_mag[y][x] > sobel_mag[y-1][x] && sobel_mag[y][x] > sobel_mag[y+1][x] )
                        canvas[y][x] = 1;
                    else
                        canvas[y][x] = 0;
                }
                else if( sobel_dir[y][x] < -22.5){ //-45
                    if( sobel_mag[y][x] > sobel_mag[y-1][x-1] && sobel_mag[y][x] > sobel_mag[y+1][x+1] )
                        canvas[y][x] = 1;
                    else
                        canvas[y][x] = 0;
                }
                else if( sobel_dir[y][x] < 22.5){ // 0
                    if( sobel_mag[y][x] > sobel_mag[y][x-1] && sobel_mag[y][x] > sobel_mag[y][x+1] )
                        canvas[y][x] = 1;
                    else
                        canvas[y][x] = 0;
                }
                else if( sobel_dir[y][x] < 67.5){ //45
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
    void doubleThreshold(int t1, int t2){
        int** sobel_mag = sobel_magnitude();
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
        }
    }

};
int main() {
    string name = "image.ppm";
    Canvas c(name); cout <<"loaded image \n";
    c.nonMaximalSupression(); cout <<"performed nonMaximalSupression \n";
    c.makePPM("imagenms.ppm",1);cout <<"created PPM \n";
    Canvas d(name);
    d.doubleThreshold(100,200);cout <<"performed double threshold \n";
    d.makePPM("imagedt.ppm",1);cout <<"created PPM \n";
    int height = c.getHeight();
    int width = c.getWidth();

    Canvas f(height,width);

    for(int r = 0; r < height; r++){
        for(int col = 0; col < width; col++){
            if(c.getCanvas()[r][col] == 1 && d.getCanvas()[r][col] == 1){
                f.getCanvas()[r][col] = 1;
            }
            else
                f.getCanvas()[r][col] = 0;
        }
    }
    f.makePPM("imagef.ppm",1);
}
