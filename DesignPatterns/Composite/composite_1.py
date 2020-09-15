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