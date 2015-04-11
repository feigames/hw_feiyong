# -*- encoding: utf-8 -*-
# __author__ = feigames@qq.com
##############################################################################
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

{
    'name' : '海外公司费用报销系统',  #模块名称
    'version' : '8.0',    
    'description' : '''   
    海外公司费用报销系统模块
    实现多公司
    预算管控 
    版本 1.0.1
    ''',
    'author' : 'feigames@qq.com',
    'website' : 'feigames@qq.com',
    'depends' : ['mail','hw_base'],
    'data' : [          #此处的xml文件如果menu跟action还有form等分开放，需要注意先后顺序
                 'views/hw_feiyong_view.xml',
                 'views/hw_feiyong_menu.xml',
                 'sequence/hw_feiyong_sequence.xml',
                 'security/hw_feiyong_security.xml',
                 'security/ir.model.access.csv',
                 'workflow/hw_feiyong_baoxiao_wf.xml',
                 'reports/hw_feiyong_baoxiao_report.xml',
                 'reports/hw_feiyong_baoxiao_report_view.xml'

    ],
    'installable' : True,
    'certificate' : '',
    'category' : '',
    'application': True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: