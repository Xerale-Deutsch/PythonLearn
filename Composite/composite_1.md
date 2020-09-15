# 组合模式_1

    按照定义来说，组合模式是将对象组合成树形结构表示，使得客户端对单个对象和组合对象的使用具有一致性。组合模式的使用通常
    会生成一颗对象树，对象树中的叶子结点代表单个对象，其他节点代表组合对象。调用某一组合对象的方法，其实会迭代调用所有其
    叶子对象的方法。
    
    使用组合模式的经典例子是 Linux 系统内的树形菜单和文件系统。在树形菜单中，每一项菜单可能是一个组合对象，其包含了菜单
    项和子菜单，这样就形成了一棵对象树。在文件系统中，叶子对象就是文件，而文件夹就是组合对象，文件夹可以包含文件夹和文件，
    同样又形成了一棵对象树。同样的例子还有员工和领导之间的关系。
    
```python
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import abc


class Worker(metaclass=abc.ABCMeta):
    """
    员工抽象类
    """
    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def work(self):
        pass


class Employee(Worker, metaclass=abc.ABCMeta):
    """
    员工类
    """
    def work(self):
        print("Employee: %s start to work " % self.name)


class Leader(Worker):
    """
    领导类
    """
    def __init__(self, name):
        self.members = []
        super(Leader, self).__init__(name)

    def add_member(self, employee):
        if employee not in self.members:
            self.members.append(employee)

    def remove_member(self, employee):
        if employee in self.members:
            self.members.remove(employee)

    def work(self):
        print("Leader: %s start to work" % self.name)
        for employee in self.members:
            employee.work()


if __name__ == '__main__':
    employee_1 = Employee("employee_1")
    employee_2 = Employee("employee_2")
    leader_1 = Leader("leader_1")
    leader_1.add_member(employee_1)
    leader_1.add_member(employee_2)

    employee_3 = Employee("employee_3")
    leader_2 = Leader("leader_2")
    leader_2.add_member(employee_3)
    leader_2.add_member(leader_1)

    leader_2.work()

```

    运行结果：
    Leader: leader_2 start to work
    Employee: employee_3 start to work 
    Leader: leader_1 start to work
    Employee: employee_1 start to work 
    Employee: employee_2 start to work 
    
    在以上的代码中，雇员和领导都属于员工，都会实现Worker.work()方法，只要执行了该方法就代表这个员工开始工作了。
    我们也注意到一个领导名下，可能有多个次级领导和其他雇员，如果一个领导开始工作，那这些次级领导和雇员都需要开工。
    员工和领导组成了一个对象树，领导是组合对象，员工是叶子对象。还可以看到 Leader类通常会实现类似于Leader.add_member
    的方法来用于添加另一个组合对象或者是叶子对象，并且调用组合对象的Leader.work方法会遍历调用（通过迭代器）其子
    对象work方法。客户端使用组合模式实现的对象时，不必关心自己处理的是单个对象还是组合对象，降低了客户端的使用难
    度，降低了耦合性。
    