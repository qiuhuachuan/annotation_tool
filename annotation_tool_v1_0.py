#!/usr/bin/env python3
# coding=utf-8
# author: Qiu Huachuan
# Date: 2020-10-19

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.pack()
        self.create_widgets()  # 初始化窗口属性
        self.correct_data_list = []
        self.correct_data_counter = 0.0
        self.other_data_list = []
        self.other_data_counter = 0.0
        self.original_data_list = []

        self.dir_and_name_of_file = askopenfilename()  # 文件路径和文件名
        # 文件路径
        self.dir_of_file = os.path.dirname(self.dir_and_name_of_file) + '/'
        # print(self.dir_of_file)
        memory_flag, final_memory_index = read_file(
            self.dir_and_name_of_file, instance=self)  # 文件读取
        # print(memory_flag)

        # 初始化数据显示
        self.current_data_index = 0
        if memory_flag:  # 存在存档情况
            self.current_line_data = self.original_data_list[final_memory_index].rstrip(
                '#')
            self.original_data_scrolledtext.insert(
                1.0, self.current_line_data)
            self.current_data_index = final_memory_index
        else:  # 不存在存档情况
            self.current_line_data = self.original_data_list[0]
            self.original_data_scrolledtext.insert(
                1.0, self.current_line_data)

    def next_line(self):
        try:
            self.current_data_index += 1
            if 0 <= self.current_data_index < len(self.original_data_list):
                self.current_line_data = self.original_data_list[self.current_data_index]
                self.original_data_scrolledtext.delete(1.0, tk.END)
                self.original_data_scrolledtext.insert(
                    1.0, self.current_line_data)
            else:
                self.current_data_index = len(self.original_data_list)
        except:
            pass

    def previous_line(self):
        try:
            self.current_data_index -= 1
            if 0 <= self.current_data_index < len(self.original_data_list):
                self.current_line_data = self.original_data_list[self.current_data_index]
                self.original_data_scrolledtext.delete(1.0, tk.END)
                self.original_data_scrolledtext.insert(
                    1.0, self.current_line_data)
            else:
                self.current_data_index = -1
        except:
            pass

    def create_widgets(self):
        self.master.title('DLL文本标注工具')  # 设置窗口名
        self.master.geometry('1200x600')  # 设置窗口大小

        # 设置每一个文本框的标签
        self.original_data_label = tk.Label(
            master=self.master, text='原始数据', bg='blue', fg='white')
        self.original_data_label.place(x=5, y=5)
        self.original_data_scrolledtext = tk.Text(
            master=self.master, width=50, height=5)
        self.original_data_scrolledtext.place(x=5, y=35)

        self.other_data_label = tk.Label(
            master=self.master, text='其他分类', bg='blue', fg='white')
        self.other_data_label.place(x=5, y=130)
        self.other_data_scrolledtext = tk.Text(
            master=self.master, width=50, height=25)
        self.other_data_scrolledtext.place(x=5, y=160)

        self.correct_data_label = tk.Label(
            master=self.master, text='正确分类', bg='blue', fg='white')
        self.correct_data_label.place(x=600, y=5)
        self.correct_data_scrolledtext = tk.Text(
            master=self.master, width=70, height=32)
        self.correct_data_scrolledtext.place(x=600, y=35)

        self.correct_data_button = tk.Button(
            self.master, text='添加到正确', bg='lightblue', width=20, command=self.add_to_correct_list)
        self.correct_data_button.place(x=430, y=5)

        self.other_data_button = tk.Button(
            self.master, text='添加到其他', bg='lightblue', width=20, command=self.add_to_other_list)
        self.other_data_button.place(x=430, y=40)

        self.next_data_button = tk.Button(
            self.master, text='下一条', bg='lightblue', width=20, command=self.next_line)
        self.next_data_button.place(x=430, y=75)

        self.previous_data_button = tk.Button(
            self.master, text='上一条', bg='lightblue', width=20, command=self.previous_line)
        self.previous_data_button.place(x=430, y=110)

        self.delete_correct_data_button = tk.Button(
            self.master, text='删除正确分类最后一条', bg='lightblue', width=20, command=self.delete_correct_list_last)
        self.delete_correct_data_button.place(x=430, y=145)

        self.delete_other_data_button = tk.Button(
            self.master, text='删除其他分类最后一条', bg='lightblue', width=20, command=self.delete_other_list_last)
        self.delete_other_data_button.place(x=430, y=180)

        self.save_data_button = tk.Button(
            self.master, text='保存', bg='lightblue', fg='red', width=20, command=self.save_data)
        self.save_data_button.place(x=430, y=340)

        self.quit_button = tk.Button(
            self.master, text='退出', fg='red', width=20, command=self.master.destroy)
        self.quit_button.place(x=430, y=380)

    def success_save_info(self):
        messagebox.showinfo('保存提示语', '保存成功')

    def add_to_correct_list(self):
        self.correct_data_counter += 1.0
        self.correct_data_list.append(self.current_line_data)
        self.correct_data_scrolledtext.insert(
            self.correct_data_counter, self.current_line_data + '\n')
        self.next_line()

    def add_to_other_list(self):
        self.other_data_counter += 1.0
        self.other_data_list.append(self.current_line_data)
        self.other_data_scrolledtext.insert(
            self.other_data_counter, self.current_line_data + '\n')
        self.next_line()

    def delete_correct_list_last(self):
        if len(self.correct_data_list) >= 1:
            self.correct_data_list.pop()
            self.correct_data_scrolledtext.delete(
                self.correct_data_counter, tk.END)
            self.correct_data_counter -= 1.0

    def delete_other_list_last(self):
        if len(self.other_data_list) >= 1:
            self.other_data_list.pop()
            self.other_data_scrolledtext.delete(
                self.other_data_counter, tk.END)
            self.other_data_counter -= 1.0

    def save_data(self):
        # 使用set()函数会引起原数据顺序的改变，因此保存的数据会和原数据顺序有差异
        correct_data_set = self.correct_data_list
        # other_data_set = list(set(self.other_data_list)) # 当用户修改了其他分类数据时，此数据不能使用
        current_other_data_set = self.other_data_scrolledtext.get(
            1.0, tk.END).rstrip().split('\n')
        # print(current_other_data_set)
        with open(self.dir_of_file + '正确分类数据.txt', mode='a+', encoding='utf-8') as correct_obj:
            for line in correct_data_set:
                correct_obj.write(line + '\n')
        with open(self.dir_of_file + '其他分类数据.txt', mode='a+', encoding='utf-8') as other_obj:
            for line in current_other_data_set:
                other_obj.write(line + '\n')
        with open(self.dir_and_name_of_file, mode='w', encoding='utf-8') as original_obj:
            for index, line in enumerate(self.original_data_list):
                if index == self.current_data_index:
                    original_obj.write(line + '###\n')
                else:
                    original_obj.write(line + '\n')
        self.success_save_info()


def read_file(dir_and_name_of_file, instance):
    counter = 0
    final_memory_index = 0
    memory_flag = False
    with open(file=dir_and_name_of_file, mode='r', encoding='utf-8') as file_object:
        for line in file_object:
            if read_memory(line=line):
                memory_flag = True
                final_memory_index = counter
            # yield line #  考虑到上一条和下一条功能，取消使用迭代器
            instance.original_data_list.append(line.strip())
            counter += 1
    return memory_flag, final_memory_index


def read_memory(line):  # 读档判断
    if '###' in line:
        return True


def main():
    root = tk.Tk()  # 创建应用的主窗口
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
