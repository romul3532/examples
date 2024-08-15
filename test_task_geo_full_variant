from sympy import symbols
from sympy import solve
import numpy as np


# комбинации:
# # #########################################################################################################
# ## 1:
# vertices_triangle=[[1,0,0],[0,1,0],[0,0,1]] ### вершины треугольника
# arbitrary_point=[0.001,0.001,0.001] ### координаты произвольной наблюдаемой точки, точки друг друга видят
# #########################################################################################################
# #########################################################################################################
# ## 2:
# vertices_triangle=[[1,0,0],[0,1,0],[0,0,1]] ### вершины треугольника
# arbitrary_point=[0,5,0] ### координаты произвольной наблюдаемой точки, точки друг друга не видят
# #########################################################################################################
# #########################################################################################################
# ## 3:
# vertices_triangle=[[1000,0,0],[0,1000,0],[0,0,1000]] ### вершины треугольника
# arbitrary_point=[0,5,0] ### координаты произвольной наблюдаемой точки, точки друг друга видят
# #########################################################################################################
# #########################################################################################################
# ## 4:
# vertices_triangle=[[1000,0,0],[0,1000,0],[0,0,1000]] ### вершины треугольника
# arbitrary_point=[0,5000,0] ### координаты произвольной наблюдаемой точки, точки друг друга не видят
# #########################################################################################################
############################## Более сложные примеры :
# #########################################################################################################
# ## 5:
# vertices_triangle=[[0,2,3],[1,5,3],[1,2,9]] ### вершины треугольника
# arbitrary_point=[0,5000,0] ### координаты произвольной наблюдаемой точки, точки друг друга не видят
# #########################################################################################################
#########################################################################################################
## 6:
vertices_triangle=[[0,2,3],[1,5,3],[1,2,9]] ### вершины треугольника
arbitrary_point=[0,0.005,0.005] ### координаты произвольной наблюдаемой точки, точки друг друга не видят
#########################################################################################################
vertices_observer=[0,0,0] ### координаты наблюдателя

'''
Описание:
    план решения задачи следующий:
      I.
        а) уравнение прямой, проходящей через две точки выглядит следующим образом:
          (x-x2)/(x2-x1)=(y-y2)/(y2-y1)=(z-z2)/(z2-z1)
          или (x-x2)/a_x=(y-y2)/a_y=(z-z2)/a_z
       б) нормаль к прямой из пункта а) задается в виде p=(a_x,a_y,a_z)
      II.
        а) уравнение плоскости по трем заданным точкам M(x1,y1,z1), N(x2,y2,z2), L(x3,y3,z3)
           можно получить из решения детерминанта:
               Ix-x0 x1-x0 x2-x0I
               Iy-y0 y1-y0 y2-y0I
               Iz-z0 z1-z0 z2-z0I
           в виде А*х+В*у+С*z+1=0
        б) нормаль к плоскости задается как: n=(A,B,C)
      III.
        Из I и II можно определить взаимное расположение прямой и плоскости:
            если скалярное произведение векторов n и p (скалярное произведение векторов=n*p) не равно 0 , 
            то у прямой и плоскости есть точка пересечения
            если скалярное произведение векторов n и p (скалярное произведение векторов=n*p) равно 0 , 
            то у прямой и плоскости нет точки пересечения
'''

def get_mutual_arrangement(vertices_triangle,vertices_observer,arbitrary_point):
    def get_direction_vector(vertices_observer,arbitrary_point):
        ### данная функция рассчитывает нормаль к прямой задаваемой двумя точками
        '''
        входные параметры:
            координаты наблюдателя (переменная vertices_observer, type(vertices_observer)=list)
            и
            координаты произвольной наблюдаемой точки (переменная arbitrary_point, type(arbitrary_point)=list)
        выходные параметры:
            переменная direction_vector (нормаль к прямой, type(direction_vector)=list)
        '''
        # a_x=vertices_observer[0]-arbitrary_point[0]
        # a_y=vertices_observer[1]-arbitrary_point[1]
        # a_z=vertices_observer[2]-arbitrary_point[2]
        direction_vector=[vertices_observer[0]-arbitrary_point[0],vertices_observer[1]-arbitrary_point[1],vertices_observer[2]-arbitrary_point[2]]
        return direction_vector
    
    def get_normal_plane(vertices_triangle):
        ### данная функция рассчитывает нормаль к плоскости задаваемой координатами трех точек
        '''
        входные параметры:
            координаты наблюдателя (переменная vertices_triangle, type(vertices_triangle)=list)
        выходные параметры:
            переменная normal_plane(нормаль к плоскости, type(normal_plane)=list)
        '''
        A,B,C=symbols('A,B,C')
        ### составление уравнений прямых для каждой пары точек, чтобы потом решить детерминант IIа
        ### первое уравнение
        equation_one=A*vertices_triangle[0][0]+B*vertices_triangle[0][1]+C*vertices_triangle[0][2]+1
        ### второе уравнение
        equation_two=A*vertices_triangle[1][0]+B*vertices_triangle[1][1]+C*vertices_triangle[1][2]+1
        ### третье уравнение
        equation_three=A*vertices_triangle[2][0]+B*vertices_triangle[2][1]+C*vertices_triangle[2][2]+1
        fse=[equation_one,equation_two,equation_three]
        ### решение вышеуказанных уравнений
        result_solve=solve(fse, [A,B,C], dict=True)
        ### определение нормали к плоскости
        normal_plane=[result_solve[0][A],result_solve[0][B],result_solve[0][C]]
        return normal_plane

    def get_relative_position_normals(direction_vector,normal_plane):
        ### данная функция рассчитывает взаимное расположение между нормалью (к прямой) и нормалью (к плоскости)
        '''
        входные параметры:
            нормаль к прямой (переменная direction_vector) и нормаль к плоскости (переменная normal_plane), (type(direction_vector)=list,
                                                                                                             type(normal_plane)=list)
        выходные параметры:
            логическая переменная result_mutual_arrangement (True или False)
        '''
        mutual_arrangement=direction_vector[0]*normal_plane[0]+direction_vector[1]*normal_plane[1]+direction_vector[2]*normal_plane[2]
        if np.round(np.float64(mutual_arrangement), decimals=2)==0: ## прямая не пересекает треугольник , значит две точки друг друга видят
            result_mutual_arrangement=True
        else: ## прямая пересекает треугольник , значит две точки друг друга не видят
            result_mutual_arrangement=False
        return result_mutual_arrangement
    

     
    def control_function(vertices_triangle,vertices_observer,arbitrary_point):
        ### управляющая функция
        direction_vector=get_direction_vector(vertices_observer,arbitrary_point)
        normal_plane=get_normal_plane(vertices_triangle)
        result_mutual_arrangement=get_relative_position_normals(direction_vector,normal_plane)
        print('')
        print('result_mutual_arrangement=',result_mutual_arrangement)
        return result_mutual_arrangement
    result_mutual_arrangement=control_function(vertices_triangle,vertices_observer,arbitrary_point)
    return result_mutual_arrangement

result_mutual_arrangement=get_mutual_arrangement(vertices_triangle,vertices_observer,arbitrary_point)
