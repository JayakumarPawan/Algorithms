#include <bits/stdc++.h>

using namespace std;
const int SIZE = 800;
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
    static bool sortAngle(Point a, Point b){

    }
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
    static double distance(Point &a, Point &b){
        return pow(pow(a.getY()-b.getY(),2)+pow(a.getX()-b.getX(),2),.5);
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
    static vector<Point> sortWithAngle(vector<Point> points){
        sort(points.begin(),points.end(),)
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
        q = Point(p.getX()+1/SIZE,p.getY()+_m/SIZE);
        if(b != 0){
            m = -a/b;
        }
        else{
            m = numeric_limits<double>::infinity();
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
        a = _q.getY() - _p.getY();
        b = _p.getX() - _q.getX();
        c = a * _p.getX() + b * _p.getY();
        if(b != 0){
            m = -a/b;
        }
        else{
            m = numeric_limits<double>::infinity();
        }
    }
    Line(Point& _p, Point& _q){
        a = _q.getY() - _p.getY();
        b = _p.getX() - _q.getX();
        c = a * _p.getX() + b * _p.getY();
        if(b != 0){
            m = -a/b;
        }
        else{
            m = numeric_limits<double>::infinity();
        }
        p = _p;
        q = _q;
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
public:
    Canvas(int _size){
        size = _size;
        canvas = new int*[SIZE];
        for(int i =0; i < SIZE; i++){
            canvas[i] = new int[SIZE];
        }
        clear();
    }
    void clear(){
        for(int y = 0; y < SIZE; y++){
            for(int x = 0; x < SIZE; x++){
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
            if(yc+y <SIZE && yc+y >=0 && xc+x < SIZE && xc+x >= 0) canvas[yc+y][xc+x] = color;
            if(yc-y <SIZE && yc-y >=0 && xc+x < SIZE && xc+x >= 0) canvas[yc-y][xc+x] = color;
            if(yc+y <SIZE && yc+y >=0 && xc-x < SIZE && xc-x >= 0) canvas[yc+y][xc-x] = color;
            if(yc-y <SIZE && yc-y >=0 && xc-x < SIZE && xc+x >= 0) canvas[yc-y][xc-x] = color;
            if(yc+x <SIZE && yc+x >=0 && xc+y < SIZE && xc+y >= 0) canvas[yc+x][xc+y] = color;
            if(yc-x <SIZE && yc-x >=0 && xc+y < SIZE && xc+y >= 0) canvas[yc-x][xc+y] = color;
            if(yc+x <SIZE && yc+x >=0 && xc-y < SIZE && xc-y >= 0) canvas[yc+x][xc-y] = color;
            if(yc-x <SIZE && yc-x >=0 && xc-y < SIZE && xc-y >= 0) canvas[yc-x][xc-y] = color;
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
            if(y1 <SIZE && y1 >=0 && x1 < SIZE && x1 >= 0) canvas[y1][x1] = color;
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
    void makePPM(string name){
        ofstream img (name);
        img << "P3 ";
        img << SIZE << " " << SIZE << " ";
        img << "1" << endl;
        for(int y = 0; y < SIZE; y++){
            for(int x = 0; x < SIZE; x++){
                if(canvas[y][x] == 2){
                    img << "1 0 0 "; //red
                }
                if(canvas[y][x] == 0){
                    img << "0 0 0 "; //black
                }
                if(canvas[y][x] == 1){
                    img << "1 1 1 "; //white
                }
                if(canvas[y][x] == 3){
                    img << "0 1 0 "; //green
                }
                if(canvas[y][x] == 4){
                    img << "0 0 1 "; //blue
                }
                if(canvas[y][x]== 5){
                    img << "1 0 1";
                }
            }
        }
        //cout << "done\n";
    }

};

int outSideHull(Line &l, Point c){ //1 if point is above and -1 if point is below
    double val = l.calcY(c) - c.getY();
    if (val == 0) return 0;
    return (val > 0) ? 1:-1;

}
vector<Point> quickHull(vector<Point>& points, Line& sep, int s){
    double max = -1.9;
    Point a = sep.getP();
    Point b = sep.getQ();
    cout <<"a  b side:";
    sep.printEnd(); cout<< (int)s<<endl;
    Point maxP = points.at(0);
    vector<Point> outside;
    for(auto & point: points){
        cout<<"\t"<< point.getX()<<" " << point.getY();
        int side = outSideHull(sep,point);
        cout <<" side:"<< side << endl;
        if(side == s){
            outside.push_back(point);
            double dist = Line::distPointToLine(sep, point);
            if(dist > max){
                max = dist;
                maxP = point;
            }
        }
    }
    maxP.print();cout <<" <-farthest point"<< endl;
    vector<Point> hull;
    if( max < 0) { //no points left outside the line
        hull.push_back(b);
        printf("\tbase-case\n");
        return hull;
    }
    Line one(a, maxP);
    Line two(maxP, b);
    printf("recur left:\n");
    vector<Point> left = quickHull(outside, one, s);
    printf("recur right:\n");
    vector<Point> right = quickHull(outside,two, s);
    hull.insert(hull.end(), left.begin(),left.end());
    hull.insert(hull.end(), right.begin(), right.end());
    return hull;

}
void part1(vector<Point> &points,vector<Point> &hull){
    points = Point::sortWithX(points);
    Point a = points.at(0);
    hull.push_back(a);
    Point b =points.at(points.size()-1);

    Line sep(a,b);
    vector<Point> left = quickHull(points,sep,1);
    Line sep2(b, a);
    vector<Point> right = quickHull(points,sep2,-1);
    hull.insert(hull.end(), left.begin(),left.end());
    hull.insert(hull.end(), right.begin(), right.end());
}
int main(){
    Canvas c(SIZE);
    srand(time(NULL));
    vector<Point> points;
    int numPoints = 50;
    points.reserve(numPoints);
//    points.emplace_back(Point(0.1,0.3));
//    points.emplace_back(Point(0.6,0.3));
//    points.emplace_back(Point(0.15,0.6));
//    points.emplace_back(Point(0.5,0.6));
//    points.emplace_back(Point(0.2,0.3));
//    points.emplace_back(Point(0.2,0.1));
    for( int i = 0; i < numPoints; ++i){
        points.emplace_back(Point());
    }
    vector<Point> hull;
    hull.reserve(numPoints);

    part1(points,hull);



    for(auto & point : points){
        c.draw(point,0);
    }
    for(int i =1; i < hull.size(); i++){
        hull.at(i).print();
        c.draw(hull.at(i), hull.at(i-1) ,2);
    }
    c.makePPM("hull.ppm");



}
