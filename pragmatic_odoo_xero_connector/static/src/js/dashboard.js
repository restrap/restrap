odoo.define('pragmatic_odoo_xero_connector.meeting_chart', function(require) {
'use strict';
	var AbstractAction = require('web.AbstractAction');
	var core = require('web.core');
	var session = require('web.session');
	var rpc = require('web.rpc');
	var Widget = require('web.Widget');
    var Dialog = require('web.Dialog');
    var _t = core._t;
    var QWeb = core.qweb;

	var XeroDashboardViewNew = AbstractAction.extend({

		template : 'XeroDashboardViewNew',
		events: {
        "click #pending_order": "on_pending_order",
        "click #completed_order": "on_completed_order",
        "click #unpaid_order": "on_unpaid_order",
        "click #paid_order": "on_paid_order",
        "click #pending_sale_order": "on_pending_sale_order",
        "click #completed_sale_order": "on_completed_sale_order",
        "click #unpaid_sale_order": "on_unpaid_sale_order",
        "click #paid_sale_order": "on_paid_sale_order",
        "click #pending_invoice": "on_pending_invoice",
        "click #completed_invoice": "on_completed_invoice",
        "click #paid_invoice": "on_paid_invoice",
        "click #unpaid_invoice": "on_unpaid_invoice",
        "click #pending_bill": "on_pending_bill",
        "click #completed_bill": "on_completed_bill",
        "click #paid_bill": "on_paid_bill",
        "click #unpaid_bill": "on_unpaid_bill",

        "click #DataType": "on_DataType",
        "click #TimeData": "on_DataType",
        "click #DataType1": "on_DataType1",
        "click #TimeData1": "on_DataType1",
        "click #DataType2": "on_DataType2",
        "click #TimeData2": "on_DataType2",
        "click #DataType3": "on_DataType3",
        "click #TimeData3": "on_DataType3",



        },

        init: function(parent, action) {
        this.actionManager = parent;
        return this._super.apply(this, arguments);
        },

        open_co_living_record: function(e){

        $('.o_stock_reports_table').show();
        },





//        DYNAMIC CHART
        on_DataType : function(){
        var element = document. getElementById('TimeData').value;
        rpc.query({model:'purchase.order',
			           method:'get_waiting_bill_counts',
			           args: [element],
			           }).then(function(res) {
                $('#completed_bill').text(res)
                var waiting_bill=res

					rpc.query({model:'account.move',
			           method:'get_unpaid_bill_counts',
			           args: [element],
			           }).then(function(res) {
                $('#unpaid_order').text(res)
                var unpaid_order=res

					rpc.query({model:'account.move',
			           method:'get_paid_bill_counts',
			           args: [element],
			           }).then(function(res) {
                $('#paid_order').text(res)
                var paid_order=res

					   rpc.query({model:'purchase.order',
			           method:'get_pending_order_counts',
			           args: [element],
			           }).then(function(res) {
                $('#pending_order').text(res)
                var total_order=res

        rpc.query({model:'purchase.order',
			           method:'purchase_piechart_detail',
			           args: [total_order,paid_order,unpaid_order,waiting_bill],
			           }).then(function(res) {
			           var charttype=document.getElementById("DataType").value;
            google.charts.load('current', {'packages':['corechart']});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {
            var data = google.visualization.arrayToDataTable(res);

   if (charttype == 'pie') {
                var options = {
                    is3D:true
                         };

                    var chart = new google.visualization.PieChart(document.getElementById('chartContainer'));
                    chart.draw(data, options);
                } else if (charttype == 'bar') {
                  var options = {
                };
                    var chart = new google.visualization.BarChart(document.getElementById('chartContainer'));
                      chart.draw(data, options);
                    } else {
                      var options = {
                      legend: 'none'
                    };
                    // Draw
                    var chart = new google.visualization.ScatterChart(document.getElementById('chartContainer'));
                    chart.draw(data, options);
                }

            }


//            PURCHASE TABLE ON CLICK
        var element = document. getElementById('TimeData').value;
        $('.as_today_meeting_table .today_meeting_line').remove();
        rpc.query({model:'purchase.order',
            method:'get_purchase_order_details',
            args: [element],
            }).then(function(rec) {
                if(rec.quotation_number){
                    for (var j = 0; j < rec.quotation_number.length; j++) {

                    var tr = '';
                   $('.as_today_meeting_table tbody').append('<tr class="today_meeting_line"><td class="o_report_line_header29"><span>'+ rec.quotation_number[j] +'</span></td><td class="o_report_line_header29"><span>'+ rec.create_date[j] +'</span></td><td class="o_report_line_header29"><span>'+ rec.total[j] +'</span></td></tr>')
                   }
               }
		});
			});
		});
		});
		});
		   });
        },


        on_DataType1 : function(){
                       var element = document. getElementById('TimeData1').value;
                       		       rpc.query({model:'sale.order',
			           method:'get_pending_sale_order_counts',
			           args: [element],
			           }).then(function(res) {
                $('#pending_sale_order').text(res)
                var sale_order = res

				rpc.query({model:'sale.order',
			           method:'get_waiting_invoice_counts',
			           args: [element],
			           }).then(function(res) {
                $('#completed_invoice').text(res)
                var waiting_sale = res


							rpc.query({model:'account.move',
			           method:'get_unpaid_invoice_counts',
			           args: [element],
			           }).then(function(res) {
                $('#unpaid_sale_order').text(res)
                var unpaid_sale = res


								rpc.query({model:'account.move',
			           method:'get_paid_invoice_counts',
			           args: [element],
			           }).then(function(res) {
                $('#paid_sale_order').text(res)
                var paid_sale = res

                       rpc.query({model:'sale.order',
			           method:'sale_piechart_detail',
			           args: [paid_sale,unpaid_sale,waiting_sale,sale_order],
			           }).then(function(res) {

			           var charttype=document.getElementById("DataType1").value;

			           google.charts.load('current', {'packages':['corechart']});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {
            var data = google.visualization.arrayToDataTable(res);

   if (charttype == 'pie') {
                var options = {
                    is3D:true
                         };

                    var chart = new google.visualization.PieChart(document.getElementById('chartContainer1'));
                    chart.draw(data, options);
                } else if (charttype == 'bar') {
                  var options = {
                };
                    var chart = new google.visualization.BarChart(document.getElementById('chartContainer1'));
                      chart.draw(data, options);
                    } else {
                      var options = {
                      legend: 'none'
                    };
                    // Draw
                    var chart = new google.visualization.ScatterChart(document.getElementById('chartContainer1'));
                    chart.draw(data, options);
                }

            }



		});
				});
		});
		});
		});
	    $('.as_today_meeting_table1 .today_meeting_line').remove();
        rpc.query({model:'sale.order',
            method:'get_sale_order_details',
            args: [element],
            }).then(function(rec) {
                if(rec.quotation_number){
                    for (var j = 0; j < rec.quotation_number.length; j++) {

                    var tr = '';
                   $('.as_today_meeting_table1 tbody').append('<tr class="today_meeting_line"><td class="o_report_line_header29"><span>'+ rec.quotation_number[j] +'</span></td><td class="o_report_line_header29"><span>'+ rec.create_date[j] +'</span></td><td class="o_report_line_header29"><span>'+ rec.total[j] +'</span></td></tr>')
                   }
               }
		});

        },

        on_DataType2 : function(){
                var element = document. getElementById('TimeData2').value;
                rpc.query({model:'account.move',
			           method:'get_pending_invoice_counts',
			           args: [element],
			           }).then(function(res) {
                $('#pending_invoice').text(res)
                var total_invoice= res


						rpc.query({model:'account.move',
			           method:'get_xero_unpaid_invoice_counts',
			           args: [element],
			           }).then(function(res) {
                $('#unpaid_invoice').text(res)
                var unpaid_invoice=res


							rpc.query({model:'account.move',
			           method:'get_xero_paid_invoice_counts',
			           args: [element],
			           }).then(function(res) {
                $('#paid_invoice').text(res)
                var paid_invoice = res

                rpc.query({model:'account.move',
			           method:'invoice_piechart_detail',
			           args: [paid_invoice,unpaid_invoice,total_invoice],
			           }).then(function(res) {

			           var charttype=document.getElementById("DataType2").value;
			           google.charts.load('current', {'packages':['corechart']});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {
            var data = google.visualization.arrayToDataTable(res);

   if (charttype == 'pie') {
                var options = {
                    is3D:true
                         };

                    var chart = new google.visualization.PieChart(document.getElementById('chartContainer2'));
                    chart.draw(data, options);
                } else if (charttype == 'bar') {
                  var options = {
                };
                    var chart = new google.visualization.BarChart(document.getElementById('chartContainer2'));
                      chart.draw(data, options);
                    } else {
                      var options = {
                      legend: 'none'
                    };
                    // Draw
                    var chart = new google.visualization.ScatterChart(document.getElementById('chartContainer2'));
                    chart.draw(data, options);
                }

            }

		});
			});
		});
		});
		$('.as_today_meeting_table2 .today_meeting_line').remove();
        rpc.query({model:'account.move',
            method:'get_invoice_details',
            args: [element],
            }).then(function(rec) {
                if(rec.quotation_number){
                    for (var j = 0; j < rec.quotation_number.length; j++) {

                    var tr = '';
                   $('.as_today_meeting_table2 tbody').append('<tr class="today_meeting_line"><td class="o_report_line_header29"><span>'+ rec.quotation_number[j] +'</span></td><td class="o_report_line_header29"><span>'+ rec.create_date[j] +'</span></td><td class="o_report_line_header29"><span>'+ rec.total[j] +'</span></td></tr>')
                   }
               }
		});



        },

        on_DataType3 : function(){
                        var element = document. getElementById('TimeData3').value;
                        		                  rpc.query({model:'account.move',
			           method:'get_pending_bill_counts',
			           args: [element],
			           }).then(function(res) {
                $('#pending_bill').text(res)
                var bill_total = res


						rpc.query({model:'account.move',
			           method:'get_unpaid_xero_bill_counts',
			           args: [element],
			           }).then(function(res) {
                $('#unpaid_bill').text(res)
                var unpaid = res


						rpc.query({model:'account.move',
			           method:'get_paid_xero_bill_counts',
			           args: [element],
			           }).then(function(res) {
                $('#paid_bill').text(res)
                var paid =res

                        rpc.query({model:'account.move',
			           method:'bill_piechart_detail',
			           args: [paid,unpaid,bill_total],
			           }).then(function(res) {

			           var charttype=document.getElementById("DataType3").value;

			           			           google.charts.load('current', {'packages':['corechart']});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {
            var data = google.visualization.arrayToDataTable(res);

   if (charttype == 'pie') {
                var options = {
                    is3D:true
                         };

                    var chart = new google.visualization.PieChart(document.getElementById('chartContainer3'));
                    chart.draw(data, options);
                } else if (charttype == 'bar') {
                  var options = {
                };
                    var chart = new google.visualization.BarChart(document.getElementById('chartContainer3'));
                      chart.draw(data, options);
                    } else {
                      var options = {
                      legend: 'none'
                    };
                    // Draw
                    var chart = new google.visualization.ScatterChart(document.getElementById('chartContainer3'));
                    chart.draw(data, options);
                }

            }

		});

		});
		});
		});

	    $('.as_today_meeting_table3 .today_meeting_line').remove();
        rpc.query({model:'account.move',
            method:'get_bill_details',
            args: [element],
            }).then(function(rec) {
                if(rec.quotation_number){
                    for (var j = 0; j < rec.quotation_number.length; j++) {

                    var tr = '';
                   $('.as_today_meeting_table3 tbody').append('<tr class="today_meeting_line"><td class="o_report_line_header29"><span>'+ rec.quotation_number[j] +'</span></td><td class="o_report_line_header29"><span>'+ rec.create_date[j] +'</span></td><td class="o_report_line_header29"><span>'+ rec.total[j] +'</span></td></tr>')
                   }
               }
		});



        },


//ON CLICK PURCHASE ORDER

        on_pending_order : function(){
        var element = document. getElementById('TimeData').value;
          let context = this;
        rpc.query({model:'purchase.order',
			           method:'get_purchase_id',
			           args: [element],
			           }).then(function(res) {
        context.do_action({
                name: _t('Purchase Order'),
                views: [[false, 'list']],
                view_type: 'form',
                view_mode: 'tree,form',
                res_model: 'purchase.order',
                type: 'ir.actions.act_window',
                target: 'current',
                domain : [["id", "in", res]],
            });
            });

        },

        on_completed_order : function(){
        this.do_action({
                name: _t('Purchase Order'),
                views: [[false, 'list']],
                view_type: 'form',
                view_mode: 'tree,form',
                res_model: 'purchase.order',
                type: 'ir.actions.act_window',
                target: 'current',
                domain : ['&',["state", "=", "done"],["xero_purchase_id", "!=", false]],
            });

        },

        on_paid_order : function(){
        var element = document. getElementById('TimeData').value;
          let context = this;
        				rpc.query({model:'account.move',
			           method:'get_paid_bill_id',
			           args: [element],
			           }).then(function(res) {
        context.do_action({
                name: _t('Bill'),
                views: [[false, 'list'], [false, 'form']],
                view_type: 'form',
                view_mode: 'tree,form',
                res_model: 'account.move',
                type: 'ir.actions.act_window',
                target: 'current',
                domain : [["id", "in",res]],
            });
            	});

        },

        on_unpaid_order : function(){
        var element = document. getElementById('TimeData').value;
          let context = this;
          				rpc.query({model:'account.move',
			           method:'get_unpaid_bill_id',
			           args: [element],
			           }).then(function(res) {
        context.do_action({
                name: _t('Bill'),
                views: [[false, 'list']],
                view_type: 'form',
                view_mode: 'tree,form',
                res_model: 'account.move',
                type: 'ir.actions.act_window',
                target: 'current',
                domain : [["id", "in", res]],
            });
            });

        },



//        ON CLICK SALE ORDER


        on_completed_invoice : function(){
        var element = document. getElementById('TimeData1').value;
        let context = this;
        rpc.query({model:'sale.order',
			           method:'get_waiting_invoice_id',
			           args: [element],
			           }).then(function(res) {
			           localStorage.res = res;
			           context.do_action({
                            name: _t('Invoice'),
                            views: [[false, 'list']],
                            view_type: 'form',
                            view_mode: 'tree,form',
                            res_model: 'sale.order',
                            type: 'ir.actions.act_window',
                            target: 'current',
                            domain : [["id", "=", res]],
                        });
			            });
        },






        on_pending_sale_order : function(){
        var element = document. getElementById('TimeData1').value;
        let context = this;
                rpc.query({model:'sale.order',
			           method:'get_pending_sale_order_id',
			           args: [element],
			           }).then(function(res) {
        context.do_action({
                 name: _t('Sale Order'),
                views: [[false, 'list']],
                view_type: 'form',
                view_mode: 'tree,form',
                res_model: 'sale.order',
                type: 'ir.actions.act_window',
                target: 'current',
                domain : [["id", "in", res]],
            });
            		});

        },

        on_completed_sale_order : function(){
        this.do_action({
                name: _t('Sale Order'),
                views: [[false, 'list']],
                view_type: 'form',
                view_mode: 'tree,form',
                res_model: 'sale.order',
                type: 'ir.actions.act_window',
                target: 'current',
                domain : ['&',["state", "=", "done"],["xero_sale_id", "!=", false]],
            });

        },

        on_paid_sale_order : function(){
        var element = document. getElementById('TimeData1').value;
          let context = this;
        					rpc.query({model:'account.move',
			           method:'get_paid_invoice_id',
			           args: [element],
			           }).then(function(res) {
        context.do_action({
                name: _t('Invoice'),
                views: [[false, 'list']],
                view_type: 'form',
                view_mode: 'tree,form',
                res_model: 'account.move',
                type: 'ir.actions.act_window',
                target: 'current',
                domain : [["id", "=", res]],
            });
            		});

        },

        on_unpaid_sale_order : function(){
        var element = document. getElementById('TimeData1').value;
          let context = this;
          			    rpc.query({model:'account.move',
			           method:'get_unpaid_invoice_id',
			           args: [element],
			           }).then(function(res) {
        context.do_action({
                name: _t('Invoice'),
                views: [[false, 'list']],
                view_type: 'form',
                view_mode: 'tree,form',
                res_model: 'account.move',
                type: 'ir.actions.act_window',
                target: 'current',
                domain : [["id", "in", res]],
            });
            		});

        },



//        Invoice

        on_pending_invoice : function(){
        var element = document. getElementById('TimeData2').value;
          let context = this;
                      rpc.query({model:'account.move',
			           method:'get_pending_invoice_id',
			           args: [element],
			           }).then(function(res) {
        context.do_action({
                name: _t('Invoices'),
                views: [[false, 'list']],
                view_type: 'form',
                view_mode: 'tree,form',
                res_model: 'account.move',
                type: 'ir.actions.act_window',
                target: 'current',
                domain : [["id", "in", res]],
            });
            	});

        },


        on_paid_invoice : function(){
        var element = document. getElementById('TimeData2').value;
          let context = this;
        				rpc.query({model:'account.move',
			           method:'get_xero_paid_invoice_id',
			           args: [element],
			           }).then(function(res) {
        context.do_action({
                name: _t('Invoice'),
                views: [[false, 'list']],
                view_type: 'form',
                view_mode: 'tree,form',
                res_model: 'account.move',
                type: 'ir.actions.act_window',
                target: 'current',
                domain : [["id", "=",res]],
            });
            });

        },

        on_unpaid_invoice : function(){
        var element = document. getElementById('TimeData2').value;
          let context = this;
            		   rpc.query({model:'account.move',
			           method:'get_xero_unpaid_invoice_cid',
			           args: [element],
			           }).then(function(res) {
        context.do_action({
                name: _t('Invoice'),
                views: [[false, 'list']],
                view_type: 'form',
                view_mode: 'tree,form',
                res_model: 'account.move',
                type: 'ir.actions.act_window',
                target: 'current',
                domain : [["id", "in",res]],
            });
            });

        },


//        BILL


        on_pending_bill : function(){
        var element = document. getElementById('TimeData3').value;
          let context = this;
                    rpc.query({model:'account.move',
			           method:'get_pending_bill_id',
			           args: [element],
			           }).then(function(res) {
        context.do_action({
                name: _t('Bill'),
                views: [[false, 'list']],
                view_type: 'form',
                view_mode: 'tree,form',
                res_model: 'account.move',
                type: 'ir.actions.act_window',
                target: 'current',
                domain : [["id", "in", res]],
            });
            });

        },

        on_completed_bill : function(){
        var element = document. getElementById('TimeData').value;
        let context = this;
        rpc.query({model:'purchase.order',
			           method:'get_waiting_bill_id',
			           args: [element],
			           }).then(function(res) {
			           localStorage.res = res;
			           context.do_action({
                            name: _t('Bill'),
                            views: [[false, 'list']],
                            view_type: 'form',
                            view_mode: 'tree,form',
                            res_model: 'purchase.order',
                            type: 'ir.actions.act_window',
                            target: 'current',
                            domain : [["id", "=", res]],
                        });
			            });
        },

        on_paid_bill : function(){
        var element = document. getElementById('TimeData3').value;
          let context = this;
        				rpc.query({model:'account.move',
			           method:'get_paid_xero_bill_id',
			           args: [element],
			           }).then(function(res) {
        context.do_action({
                name: _t('Bill'),
                views: [[false, 'list']],
                view_type: 'form',
                view_mode: 'tree,form',
                res_model: 'account.move',
                type: 'ir.actions.act_window',
                target: 'current',
                domain : [["id", "in", res]],
            });
            });

        },

        on_unpaid_bill : function(){
        var element = document. getElementById('TimeData3').value;

          let context = this;
        				rpc.query({model:'account.move',
			           method:'get_unpaid_xero_bill_id',
			           args: [element],
			           }).then(function(res) {
        context.do_action({
                name: _t('Bill'),
                views: [[false, 'list']],
                view_type: 'form',
                view_mode: 'tree,form',
                res_model: 'account.move',
                type: 'ir.actions.act_window',
                target: 'current',
                domain : [["id", "in", res]],
            });
            	});

        },





		start : function() {
//		PURCHASE
        		            rpc.query({model:'purchase.order',
			           method:'get_pending_order_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#pending_order').text(res)
                var total_order = res


//		rpc.query({model:'purchase.order',
//			           method:'get_completed_order_counts',
//			           args: [],
//			           }).then(function(res) {
//                $('#completed_order').text(res)
                	rpc.query({model:'purchase.order',
			           method:'get_waiting_bill_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#completed_bill').text(res)
                var waiting_bill = res


				rpc.query({model:'account.move',
			           method:'get_unpaid_bill_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#unpaid_order').text(res)
                var unpaid_order = res


					rpc.query({model:'account.move',
			           method:'get_paid_bill_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#paid_order').text(res)
                var paid_order = res

		rpc.query({model:'purchase.order',
			           method:'purchase_piechart_detail',
			           args: [total_order,paid_order,unpaid_order,waiting_bill],
			           }).then(function(res) {
            google.charts.load('current', {'packages':['corechart']});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {
            var data = google.visualization.arrayToDataTable(res);

            var options = {
              is3D:true
            };

            var chart = new google.visualization.PieChart(document.getElementById('chartContainer'));
              chart.draw(data, options);
            }
            });
            });
            });
            });
            });


//		SALE

            rpc.query({model:'sale.order',
			           method:'get_pending_sale_order_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#pending_sale_order').text(res)
                var sale_order = res



//		rpc.query({model:'sale.order',
//			           method:'get_completed_sale_order_counts',
//			           args: [],
//			           }).then(function(res) {
//                $('#completed_sale_order').text(res)
        rpc.query({model:'sale.order',
			           method:'get_waiting_invoice_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#completed_invoice').text(res)
                var waiting_sale = res


				rpc.query({model:'account.move',
			           method:'get_unpaid_invoice_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#unpaid_sale_order').text(res)
                var unpaid_sale = res


					rpc.query({model:'account.move',
			           method:'get_paid_invoice_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#paid_sale_order').text(res)
                var paid_sale = res




				rpc.query({model:'sale.order',
			           method:'sale_piechart_detail',
			           args: [paid_sale,unpaid_sale,waiting_sale,sale_order],
			           }).then(function(res) {
            google.charts.load('current', {'packages':['corechart']});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {
            var data = google.visualization.arrayToDataTable(res);

            var options = {
              is3D:true
            };

            var chart = new google.visualization.PieChart(document.getElementById('chartContainer1'));
              chart.draw(data, options);
            }
            });
            });
            });
            });
            });



//		INVOICE

            rpc.query({model:'account.move',
			           method:'get_pending_invoice_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#pending_invoice').text(res)
                var total_invoice= res


						rpc.query({model:'account.move',
			           method:'get_xero_unpaid_invoice_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#unpaid_invoice').text(res)
                var unpaid_invoice=res


							rpc.query({model:'account.move',
			           method:'get_xero_paid_invoice_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#paid_invoice').text(res)
                var paid_invoice = res

				rpc.query({model:'account.move',
			           method:'invoice_piechart_detail',
			           args: [paid_invoice,unpaid_invoice,total_invoice],
			           }).then(function(res) {
            google.charts.load('current', {'packages':['corechart']});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {
            var data = google.visualization.arrayToDataTable(res);

            var options = {
              is3D:true
            };

            var chart = new google.visualization.PieChart(document.getElementById('chartContainer2'));
              chart.draw(data, options);
            }
            });
            });
            });
            });


//		BILL

                             		                  rpc.query({model:'account.move',
			           method:'get_pending_bill_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#pending_bill').text(res)
                var bill_total = res


						rpc.query({model:'account.move',
			           method:'get_unpaid_xero_bill_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#unpaid_bill').text(res)
                var unpaid = res


						rpc.query({model:'account.move',
			           method:'get_paid_xero_bill_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#paid_bill').text(res)
                var paid =res



				rpc.query({model:'account.move',
			           method:'bill_piechart_detail',
			           args: [paid,unpaid,bill_total],
			           }).then(function(res) {
            google.charts.load('current', {'packages':['corechart']});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {
            var data = google.visualization.arrayToDataTable(res);

            var options = {
              is3D:true
            };

            var chart = new google.visualization.PieChart(document.getElementById('chartContainer3'));
              chart.draw(data, options);
            }
            });
            });
            });
            });





//		PURCHASE

		       $('.as_today_meeting_table .today_meeting_line').remove();
        rpc.query({model:'purchase.order',
            method:'get_purchase_order_details',
            args: ['last_month'],
            }).then(function(rec) {
                if(rec.quotation_number){
                    for (var j = 0; j < rec.quotation_number.length; j++) {

                    var tr = '';
                   $('.as_today_meeting_table tbody').append('<tr class="today_meeting_line"><td class="o_report_line_header29"><span>'+ rec.quotation_number[j] +'</span></td><td class="o_report_line_header29"><span>'+ rec.create_date[j] +'</span></td><td class="o_report_line_header29"><span>'+ rec.total[j] +'</span></td></tr>')
                   }
               }
		});

//		SALE


		       $('.as_today_meeting_table1 .today_meeting_line').remove();
        rpc.query({model:'sale.order',
            method:'get_sale_order_details',
            args: ['last_month'],
            }).then(function(rec) {
                if(rec.quotation_number){
                    for (var j = 0; j < rec.quotation_number.length; j++) {

                    var tr = '';
                   $('.as_today_meeting_table1 tbody').append('<tr class="today_meeting_line"><td class="o_report_line_header29"><span>'+ rec.quotation_number[j] +'</span></td><td class="o_report_line_header29"><span>'+ rec.create_date[j] +'</span></td><td class="o_report_line_header29"><span>'+ rec.total[j] +'</span></td></tr>')
                   }
               }
		});


//		INVOICE

                  rpc.query({model:'account.move',
			           method:'get_pending_invoice_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#pending_invoice').text(res)

		});

		rpc.query({model:'sale.order',
			           method:'get_waiting_invoice_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#completed_invoice').text(res)

		});
				rpc.query({model:'account.move',
			           method:'get_xero_unpaid_invoice_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#unpaid_invoice').text(res)

		});
					rpc.query({model:'account.move',
			           method:'get_xero_paid_invoice_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#paid_invoice').text(res)

		});
		       $('.as_today_meeting_table2 .today_meeting_line').remove();
        rpc.query({model:'account.move',
            method:'get_invoice_details',
            args: ['last_month'],
            }).then(function(rec) {
                if(rec.quotation_number){
                    for (var j = 0; j < rec.quotation_number.length; j++) {

                    var tr = '';
                   $('.as_today_meeting_table2 tbody').append('<tr class="today_meeting_line"><td class="o_report_line_header29"><span>'+ rec.quotation_number[j] +'</span></td><td class="o_report_line_header29"><span>'+ rec.create_date[j] +'</span></td><td class="o_report_line_header29"><span>'+ rec.total[j] +'</span></td></tr>')
                   }
               }
		});


//		Bill

                  rpc.query({model:'account.move',
			           method:'get_pending_bill_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#pending_bill').text(res)

		});
		rpc.query({model:'purchase.order',
			           method:'get_waiting_bill_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#completed_bill').text(res)

		});
				rpc.query({model:'account.move',
			           method:'get_unpaid_xero_bill_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#unpaid_bill').text(res)

		});
					rpc.query({model:'account.move',
			           method:'get_paid_xero_bill_counts',
			           args: ['last_month'],
			           }).then(function(res) {
                $('#paid_bill').text(res)

		});
		       $('.as_today_meeting_table3 .today_meeting_line').remove();
        rpc.query({model:'account.move',
            method:'get_bill_details',
            args: ['last_month'],
            }).then(function(rec) {
                if(rec.quotation_number){
                    for (var j = 0; j < rec.quotation_number.length; j++) {

                    var tr = '';
                   $('.as_today_meeting_table3 tbody').append('<tr class="today_meeting_line"><td class="o_report_line_header29"><span>'+ rec.quotation_number[j] +'</span></td><td class="o_report_line_header29"><span>'+ rec.create_date[j] +'</span></td><td class="o_report_line_header29"><span>'+ rec.total[j] +'</span></td></tr>')
                   }
               }
		});









            },

		});

	core.action_registry.add('meeting_chart', XeroDashboardViewNew);
	return {
		XeroDashboardViewNew : XeroDashboardViewNew,
	};
});