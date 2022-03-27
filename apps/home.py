import streamlit as st

def app():
    st.title('ЦИФРОВЫЕ ИССЛЕДОВАНИЯ ИНТЕРТЕКСТУАЛЬНОСТИ НА МАТЕРИАЛЕ РУССКОЙ ПОЭЗИИ')
    st.header('О ПРОЕКТЕ')
    st.text("""Проект посвящен исследованию интертекстуальности на материале русской поэзии.""")
    st.text("""Этот ресурс может быть полезен как исследователям, так и непродвинутым""")
    st.text('пользователям, так как помимо узкоспециализированной информации на нем') 
    st.text('представлены научно-популярные статьи и подробная инструкция для пользователей.')
    st.text('Школьная программа не предполагает интертекстуального анализ апоэзии, поэтому')
    st.text('увлеченным литературой учащимся наш ресурс поможет открыть много нового.')
    
    st.header('НАША КОМАНДА')
    st.markdown("""
    <div class="row align-items-start" style="margin-bottom:2%">
                <div class="col">
                    <div class="d-grid gap-0">
                        <div class="circular-img mx-auto d-block">
                            <img src="../static/images/anya.jpg" class="img-fluid circular-portrait" style="margin-top:-2vh">
                        </div>
                        <div class="p-2 fs-4 fw-bold text-center lh-sm">Аксенова Анна</div>
                        <div class="p-2 fs-6 fw-lighter text-center lh-sm">Разработка автоматической разметки</div>
                    </div>
                </div>
                <!-- Person 2-->
                <div class="col">
                   <div class="d-grid gap-0">
                       <div class="circular-img mx-auto d-block">
                           <img src="../static/images/katya_v.jpg" class="img-fluid circular-portrait" style="margin-top:-5.5vh">
                       </div>
                       <div class="p-2 fs-4 fw-bold text-center lh-sm">Волошина Екатерина</div>
                       <div class="p-2 fs-6 fw-lighter text-center lh-sm">Разработка автоматической разметки</div>
                    </div>
                </div>
                <!-- Person 3 -->
                <div class="col">
                    <div class="d-grid gap-0">
                        <div class="circular-img mx-auto d-block">
                            <img src="../static/images/polina.jpg" class="img-fluid circular-portrait" style="margin-top:-2vh">
                        </div>
                        <div class="p-2 fs-4 fw-bold text-center lh-sm">Кудрявцева Полина</div>
                        <div class="p-2 fs-6 fw-lighter text-center lh-sm">Разработка автоматической разметки</div>
                    </div>
                </div>
            </div>
            <!-- Person 4 -->
            <div class="row justify-content-evenly">
                <div class="col-4">
                    <div class="d-grid gap-0">
                        <div class="circular-img mx-auto d-block">
                            <img src="../static/images/katya_tak.jpeg" class="img-fluid circular-portrait" style="margin-top:-1vh">
                        </div>
                        <div class="p-2 fs-4 fw-bold text-center lh-sm">Такташева Екатерина</div>
                        <div class="p-2 fs-6 fw-lighter text-center lh-sm">Создание корпуса и сайта, техническая поддержка</div>
                    </div>
                </div>
                <!-- Person 5 -->
                <div class="col-4">
                    <div class="d-grid gap-0">
                        <div class="circular-img mx-auto d-block">
                            <img src="../static/images/katya_tar.jpg" class="circular-landscape" style="margin-left:-1vw">
                        </div>
                        <div class="p-2 fs-4 fw-bold text-center">Тарасова Екатерина</div>
                        <div class="p-2 fs-6 fw-lighter text-center">Филологический комментарий</div>
                    </div>
                </div>""")
    
