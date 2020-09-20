# 将文本生成HTML

    格式比较简单，需要添加其他规则的话，可以自行去添加规则。
    
    1. 需要添加其他html标签，可以在handlers.py里的HTMLRender类中新增对应标签的规则，
       并在rules里添加约定好的检测规则，如li标签的'-'。
      
    2. 使用方式：python markup.py < test.txt > test.html
    
    3. 如果感觉使用复杂，可以写个一键式拖入的懒人操作。