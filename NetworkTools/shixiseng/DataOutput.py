# -*- coding: utf-8 -*-


class DataOutput(object):
    def __init__(self):
        """Save data into file."""
        self.data = []
    
    def store_data(self, data):
        if data is None:
            return
        self.data.append(data)
    
    def write(self, save_path):
        pass
    
    def save(self, savepath):
        """保存到文件"""
        postfix = os.path.splitext(savepath)[1]
        
        if postfix in ['.xls', '.xlsx', '.xlsm']:
            self.df.to_excel(savepath)
        elif postfix in ['.csv']:
            self.df.to_csv(savepath)        
        else:
            raise ValueError(f'文件格式{postfix}不支持。')
        print(f'保存到路径：{savepath}')