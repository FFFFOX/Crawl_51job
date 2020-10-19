import tools as tool


keyin = input("请输入相关的职位信息：")
start_pagein = int(input("请输入起始页面："))
end_pagein = int(input("请输入结束页面："))

tool.get_X_Y(keyin, start_pagein, end_pagein)
tool.get_Histogram(keyin, start_pagein, end_pagein)
tool.get_bar(keyin, start_pagein, end_pagein)
tool.get_Pie(keyin, start_pagein, end_pagein)