/**
 * Created by summerrain on 2017/7/20.
 */
var mCurrentPage = 0;//当前页
var mIsLoading = false;
var lineHeight = 80;
var mListView = null;

var curWt = 0;
var isLoadView = false;
var item_seq = 0;
var task_list = null;

myApp.onPageAfterAnimation('contribution-list', function (page) {
    console.log("------------------------onPageAfterAnimation-------------------------");
    if (!isLoadView) {
        initViewPage();
    }
    isLoadView = true;
});

myApp.onPageAfterBack('contribution-list', function (page) {
    mCurrentPage = 0;
    console.log("------------------------loadList-------------------------");
    loadList();
    isLoadView = false;
});

/**
 * @功能描述: 初始化
 * @作者: 黎嘉杰
 * @日期: 2017-01-12
 */
function init() {
    //绑定虚拟列表
    bindVirtualList();
    //绑定搜索栏
    bindSearchBar();
    //加载列表
    loadList();
}

/**
 * @功能描述: 绑定搜索栏
 * @作者: 黎嘉杰
 * @日期: 2017-01-12
 */
function bindSearchBar() {
    mySearchbar = myApp.searchbar(
        '.searchbar',
        {
            customSearch: true,
            onSearch: function () {
                //输入后， 重新加载列表
                loadList();
            }
        }
    );
}

/**
 * @功能描述: 绑定虚拟列表
 * @作者: 黎嘉杰
 * @日期: 2017-01-12
 */
function bindVirtualList() {
    mListView = myApp.virtualList('#task-list', {
        items: [],
        height: function (item) {
            return lineHeight;
        },
        renderItem: function (index, item) {
            return renderItem(index, item);
        },
    });

    var refreshContent = $('.pull-to-refresh-content');
    refreshContent.off('refresh');
    refreshContent.on('refresh', function (e) {
        mCurrentPage = 0;
        console.log("执行了下拉刷新");
        myApp.pullToRefreshDone();
        loadList();
        setTimeout(function () {
            myApp.pullToRefreshDone();
        }, 20000);
    });


}

/**
 * @功能描述: 渲染公告行
 * @作者: 黎嘉杰
 * @日期: 2017-01-12
 */
function renderItem(index, item) {
    var itemHtml = Template7.templates.taskItem(item);
    itemHtml = itemHtml.replace(/[\r\n]/g, "");
    itemHtml = itemHtml.trim();
    return itemHtml;
}

/**
 * @功能描述: 加载数据
 * @作者: 黎嘉杰
 * @日期: 2017-01-12
 */
function loadList() {
    var txt = $('#search-input').val();
    var params = {
        'page': mCurrentPage,
        'txt': txt
    };
    //
    // $.post('/m_ws/media/task/list', params, function(result){
    //     mIsLoading = false;
    //     myApp.pullToRefreshDone();
    //
    //     if (mCurrentPage == 0) {
    //         mListView.deleteAllItems();
    //     }
    //     result = JSON.parse(result)
    //     result = result['data'];
    //     mListView.appendItems(result);
    //
    //     $(".infinite-scroll-preloader").hide();
    // });


    mIsLoading = false;
    myApp.pullToRefreshDone();

    if (mCurrentPage == 0) {
        mListView.deleteAllItems();
    }
    var result = [
        {"task_id": "task1", "task_name": "name1", "task_type": "type1", "task_date": "date1", "id": "hello1"},
        {"task_id": "task2", "task_name": "name2", "task_type": "type2", "task_date": "date2", "id": "hello2"},
        {"task_id": "task3", "task_name": "name3", "task_type": "type3", "task_date": "date3", "id": "hello3"}
    ];
    mListView.appendItems(result);

    $(".infinite-scroll-preloader").hide();

}

$('.infinite-scroll').on('infinite', function () {
    if (mIsLoading) {
        return;
    }
    if (mCurrentPage > 10) {
        $('.infinite-scroll-preloader').hide();
        return;
    }
    mIsLoading = true;
    setTimeout(function () {
        mIsLoading = false;
        $('.infinite-scroll-preloader').hide();
    }, 20000);
    mCurrentPage++;
    loadList();
});


/**
 * @功能描述 保存确认事件
 * @参数 是否确认
 * @作者 夏雨
 * @日期 2017-06-05
 */
 function onSubmit(course_id) {
         var startTimestamp = getCookie('startTimestamp')
         $.ajax({
             type: 'post',
             data: {
                 user_id: getCookie('user_id'),
                 course_id: course_id,
                 timestamp: startTimestamp
             },
             url: 'http://10.20.113.90:8069/w/a',
             success: function(msg) {
                 if (msg === '已过期') {
                     window.location.href = 'http://10.20.113.90:8069/w/qrcode_html'
                 }

                 alert(msg)
             }
         });
 }


function onBack() {
    mainView.router.back({
        'reload': true,
        'animatePages': true
    });
}

function bindViewPageEvent() {
    $('.swipeout').on('deleted', function () {
        setTimeout("calBillAmt()", 50);
    });
}

function initViewPage() {
    console.log("执行View初始化");

    initDatePicker('sale_date');
    loadCustomerList();
    loadProductList();
    disPlay_items();
    bindViewPageEvent();
    initPound();
}


function onView(task_id) {
    mainView.router.load({
        'url': '/ws_training/body?task_id=' + task_id,
        'reload': false,
        'animatePages': true,
        'pushState': true
    });
}

function onDelete(task_id) {
    if (task_id != null && task_id != '') {
        var values = {'sale_id': task_id};

        //调用后台方法保存
        odoo.rpcCall('ws.fish.sale', 'mobile_delete', [values], {}, function (result) {
            onBack();
        })
    }
    else {
        myApp.alert("当前单据未保存， 不能删除！", "提示");
        return;
    }
}

function onLogin(username, password) {

    var startTimestamp = window.location.href.substring(window.location.href.lastIndexOf('=') + 1)
    $.ajax({
        type: 'post',
        data: {
            username: username,
            password: password
        },
        url: '/w/login',
        success: function(data) {
            var jsonResult = JSON.parse(data)
            alert(jsonResult.msg)
            if (jsonResult.login_success) {
                setCookie('user_id', jsonResult.user_id)
                setCookie('startTimestamp', startTimestamp)
                window.location.href = 'http://10.20.113.90:8069/ws_training/guide'
            }
        }
    })

}

init();
