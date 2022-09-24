#include<iostream>
#include<math.h>
#include <fstream>
#include <cstdlib>
#include <time.h>
#include<cmath>
#include<ostream>
#include <iomanip>
#include<random>
#include<string>
#include <list>
#include <iterator>
#include <vector>
#include <algorithm>
#include <sstream>
#include <unordered_map>
// #include <bits/stdc++.h>
using namespace std;
#define ss pair< unsigned long long int, unsigned long long int> //square coordinates
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
    void print(){
        cout <<"(" << x << " , " << y << ") ";
    }
    string toString(){
        return "("+std::to_string(x) + ", " + std::to_string(y)+")";
    }
    bool operator ==(Point &other){
        if(other.x - x < 0.000001 && other.y - y < 0.000001){
            return true;
        }
        return false;
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
        q = Point(p.getX()+1/SIZE,p.getY()+_m/SIZE);
        m = _m;
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
      m = -a/b;
    }
    Line(Point _p, Point _q){
        a = _q.getY() - _p.getY();
        b = _p.getX() - _q.getX();
        c = a * _p.getX() + b * _p.getY();
        m = -a/b;
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
    void print(){
        cout << "A: "<<a<< " B: "<<b<< " C: "<<c<<endl;
    }
    void printEnd(){
        cout << "A: ";
        p.print();
        cout << "B: ";
        q.print();
    }
    static Point intersection(Line &a, Line&b){
        double det = a.getA() * b.getB() - a.getB() * b.getA();
        double x = (b.getB() * a.getC() - a.getB() * b.getC())/det;
        double y = (a.getA() * b.getC() - b.getA() * a.getC())/det;
        Point p(x,y);
        return p;
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
    void setB( double val){
        b = val;
    }
    void setA( double val){
        a = val;
    }
    void setC( double val){
        c = val;
    }
};
struct hash_pair {
    template <class T1, class T2>
    size_t operator()(const pair<T1, T2>& p) const
    {
        auto hash1 = hash<T1>{}(p.first);
        auto hash2 = hash<T2>{}(p.second);
        return hash1 ^ hash2;
        //(53 + int_hash(row)) * 53 + int_hash(col)
    }
};

void makePoints(vector<Point> &points,string filename){
    ifstream f(filename);
    string line;
    while(getline(f,line)){
      if(line.length() == 1)
        break;
      int comma = line.find(' ');
      double x = stod(line.substr(0,comma));
      double y = stod(line.substr(comma+1));
      Point p(x,y);
      points.push_back(p);
    }
}
void makeFile(vector<Point> &points, string name){
  FILE *fptr = fopen(name.c_str(),"w");
  for( Point point: points){
      fprintf(fptr,"%.20g",point.getX());
      fprintf(fptr, " ");
      fprintf(fptr,"%.20g",point.getY());
      fprintf(fptr, "\n");
  }
}
void shuffle( vector<Point> & points){
  for(int i =points.size() -1; i >0;--i ){
    int j = rand() %(i+1);
    Point temp = points.at(i);
    points.at(i) = points.at(j);
    points.at(j) = temp;
  }
}
Line part4(vector<Point> & points){
    /*
    subsquare widht/height is delta/2
    divide unit square into subsquares
    dict = subsquare:point
    for next point:
        calc sub-square its in (round down for border and corner cases)
        if there is a point in it or points in the 25 squares around it,
        update delta, recalculate the subsquares and update the dictionary
        else just put it in and go next
    */
    Point p1 = points.at(0);
    Point p2 = points.at(1);
    Line minl(p1,p2);
    double delta = minl.distance();
    double d = delta/2;
    cout << "starting point: "; p1.print(); p2.print() ; cout <<endl;
    cout << "starting delta: "<<delta<<endl;
    cout << "starting square size: "<<d<<endl;
    unordered_map<ss,Point,hash_pair> dict;
     unsigned long long int sx = ( unsigned long long int) (p1.getX()/d);
     unsigned long long int sy = ( unsigned long long int) (p1.getY()/d);
    cout <<"Point 1 at "<<sx << ", " << sy <<endl;
    dict.emplace(ss(sx,sy),p1);
    sx = ( unsigned long long int) (p2.getX()/d);
    sy = ( unsigned long long int) (p2.getY()/d);
    cout <<"Point 2 at "<<sx << ", " << sy <<endl;
    dict.emplace(ss(sx,sy),p2);
    vector<int> xadj = {0,-1,-1,0,1,1 ,1 ,0 ,-1,-2,-2,-2,-1,0,1 ,2 ,2,2 ,2 ,2 ,1 ,0 ,-1,-2,-2};
    vector<int> yadj = {0, 0 ,1 ,1 ,1,0,-1,-1,-1, 0, 1, 2, 2,2 ,2,2 ,1 ,0,-1,-2,-2,-2,-2,-2,-1};
     unsigned long long int ax;
     unsigned long long int ay;
    for( auto i = points.begin()+2; i != points.end(); ++i){
        Point cur = *i;
        cout << "current point: "; cur.print() ; cout<< "current squaresize: "<<d<<endl;
        sx = ( unsigned long long int) (i->getX()/d);
        sy = ( unsigned long long int) (i->getY()/d);
        cout <<"current point at "<<sx << ", " << sy <<endl;
        for(int c = 0; c < xadj.size(); ++c){
            if(sx == 0 && xadj.at(c) <0) continue;
            if(sy == 0 && yadj.at(c) <0) continue;
            if(sx == 1 && xadj.at(c) <-1) continue;
            if(sy == 1 && yadj.at(c) <-1) continue;
            ax = sx+ xadj.at(c);
            ay = sy+ yadj.at(c);
            if(ax < (unsigned long long int)(1/d) && ay < (unsigned long long int)(1/d)){
                //cout <<"\tChecking: "<<ax << ", " << ay <<endl;
                if(dict.find(ss(ax,ay)) !=dict.end()){
                    cout << "\t\tFound existing entry" <<endl;
                    Point found = dict.at(ss(ax,ay));
                    cout << "\t\tExisting point: "; found.print() ; cout <<endl;
                    Line temp(cur,found);
                    if(temp.distance() <delta){
                        cout <<"\t\texisting point distance is smaller than delta"<<endl;
                        minl = temp;
                        delta = minl.distance();
                        d = delta/2;
                        cout << "\t\tnew delta: "<<delta<<endl;
                        cout << "\t\tnew square size: "<<d<<endl;
                        dict.clear();
                        for( auto itr = points.begin(); itr != i; ++itr){
                            sx = ( unsigned long long int) (itr->getX()/d);
                            sy = ( unsigned long long int) (itr->getY()/d);
                            dict.emplace(ss(sx,sy),*itr);
                            cout <<"\t\t"; itr->print(); cout << "now at "<<sx << ", " << sy <<endl;
                            for(auto& x: dict){
                                cout <<"\t\t"<< x.first.first <<" "<<x.first.second << " ";
                                x.second.print();
                                cout << endl;
                            }
                        }
                        break;
                    }
                }
            }
        }
        sx = ( unsigned long long int) (i->getX()/d);
        sy = ( unsigned long long int) (i->getY()/d);
        dict.emplace(ss(sx,sy),p1); //g++ -std=c++11 -o 4 lab4.cpp
        //cout << "\tplacing current point into: "<<sx << ", " << sy <<endl;
    }

    return minl;
}
main(){
  srand(time(NULL));
  vector<Point> points;
  int numPoints = 5;
  for(int i = 0; i < numPoints; ++i){
    points.push_back(Point());
  }
  shuffle(points);
  string name = "points.txt";
  makeFile(points,name);
  makePoints(points,name);
  Line ml = part4(points);
  ml.printEnd();

}
