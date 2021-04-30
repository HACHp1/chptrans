import re

a='''In this section, we propose some preliminary guiding
principles for using deep learning to detect vulnerabilities.
These principles are sufﬁcient for the present study, but may
need to be reﬁned to serve the more general purpose of deep
learning-based vulnerability detection. These principles are
centered at answering three fundamental questions: (i) How
to represent programs for deep learning-based vulnerability
detection? (ii) What is the appropriate granularity for deep
learning-based vulnerability detection? (iii) How to select a
speciﬁc neural network for vulnerability detection?
'''.replace(
            '- ', '').replace('-\r\n', '').replace('-\n', '').replace('\n', ' ').replace('\r', '').strip()
        
print(re.split('([.?])\s', a))
