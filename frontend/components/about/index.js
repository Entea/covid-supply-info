import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import {
    fetchContacts as fetchContactsAction,
    sendMessage as sendMessageAction,
    init as initAction
} from '../../actions/creators/contacts';
import { Col, Image, Row } from 'react-bootstrap'
import BlockHeader from './BlockHeader'
import Block from './Block'

class About extends Component {
    componentDidMount() {
        this.props.fetchContactsAction();
        this.props.initAction();
    }

    render() {
        const { data, sending, status, sendMessageAction } = this.props;

        return (
            <main className='about'>
                <Row>
                    <Col xs>
                        <Block filled={true}>
                            <BlockHeader>WWW.TIREK.KG</BlockHeader>
                            <p className="about__block_content">
                                «Тирек» – это открытая онлайн-платформа, где отображаются данные по оснащенности и потребностям организаций здравохранения Кыргызской Республики, медицинских работников, необходимые в борьбе с эпидемией коронавируса (COVID-19).
                            </p>
                        </Block>
                        <Block>
                            <BlockHeader>МИССИЯ ПЛАТФОРМЫ «ТИРЕК»</BlockHeader>
                            <p className="about__block_content">
                                Создание и развитие единой современной, профессиональной и открытой онлайн системы сбора информации о потребностях организаций здравоохранения Кыргызской Республики, медицинских работников, ресурсах, необходимых Кыргызской Республике в борьбе с эпидемией коронавируса (COVID-19), их обработка, а также мониторинг, анализ и синхронизация усилий всех секторов общества – государства, донорского сообщества, бизнес сообщества, частного сектора и  гражданского общества.
                            </p>
                        </Block>
                        <Block filled={true}>
                            <BlockHeader>ЦЕЛИ ПЛАТФОРМЫ «ТИРЕК»</BlockHeader>
                            <p className="about__block_content">
                                Содействие в организации адресной эффективной, качественной помощи организациям здравоохранения, медицинским работникам Кыргызской Республики на период борьбы с коронавирусом (COVID-19) через предоставление данных;
                                содействие в синхронизации усилий государства, донорского сообщества, бизнес-сектора и гражданского общества Кыргызской Республики в оказании оперативной и необходимой поддержки организациям здравоохранения и медицинским работникам;
                                создание прозрачной схемы о нуждах и потребностях отечественного здравоохранения на период борьбы с коронавирусом (COVID-19).
                                </p>
                        </Block>
                        <Block>
                            <BlockHeader>ПЛАТФОРМА «ТИРЕК» ПОЗВОЛИТ ВИДЕТЬ И ЗНАТЬ</BlockHeader>
                            <ul className="about__block_content" style={{listStyleType: "disc"}}>
                                <li>Текущую медицинскую готовность и потребность (спецодежда, медикаменты и оборудование) в борьбе с коронавирусом (COVID-19);</li>
                                <li>Данные о потребностях организаций здравоохранения и медицинских работников, необходимые Кыргызской Республике в борьбе с коронавирусом (COVID-19);</li>
                                <li>Информацию по всем видам пожертвований от донорского сообщества, бизнес сообщества, частного сектора, гражданского общества и их распределения;</li>
                                <li>Информацию о средствах, выделенные государством для борьбы с коронавирусом (COVID-19);</li>
                                <li>Мониторинг распределения гуманитарной помощи.</li>
                            </ul>
                            <Row className="about__feature_images">
                                <Col xs={6} md={3}>
                                    <Image src="/about/1.png" fluid />
                                </Col>
                                <Col xs={6} md={3}>
                                    <Image src="/about/2.png" fluid />
                                </Col>
                                <Col xs={6} md={3}>
                                    <Image src="/about/3.png" fluid />
                                </Col>
                                <Col xs={6} md={3}>
                                    <Image src="/about/4.png" fluid />
                                </Col>
                            </Row>
                        </Block>
                        <Block filled={true}>
                            <BlockHeader>КЕМ СОЗДАНА ПЛАТФОРМА «ТИРЕК»?</BlockHeader>
                            <Row>
                                {/* <Col>
                                    <Image src="/about/5.png" fluid />
                                </Col> */}
                                <Col>
                                    <p className="about__block_content">
                                        Это гражданская инициатива неравнодушных людей из IT сообщества, госсектора, бизнеса и неправительственных организаций.
                                    </p>
                                </Col>
                            </Row>
                        </Block>
                        <Block>
                            <BlockHeader>УНИКАЛЬНОСТЬ И ВАЖНОСТЬ ПЛАТФОРМЫ «ТИРЕК» ДЛЯ ВРАЧЕЙ</BlockHeader>
                            <p className="about__block_content">
                                Онлайн платформа «Тирек» -  это уникальная возможность для организаций здравоохранения Кыргызской Республики, в том числе для медицинских работников самостоятельно заполнять, отслеживать и проводить мониторинг ситуации и наличия медицинских ресурсов в своей организации.  Платформа – это усилие, нацеленное на предоставление ранее закрытых данных, отражающих как нынешнюю ситуацию в оснащенности организаций здравоохранения, так и их потребности в борьбе с эпидемией.
                                Мы надеемся, что данное решение улучшит бизнес процессы организаций здравоохранения, предоставит картину ситуации широкой общественности, а также разгрузит службу неотложной помощи.
                            </p>
                        </Block>
                        <Block filled={true} className="small-text">
                                Разработчики и координаторы онлайн платформы «ТИРЕК»
                                не несут ответственности за качество и подотчетность предоставленной помощи
                                организациям здравоохранения Кыргызской Республики и медицинским работникам.
                                Ответственность за информацию о той или иной помощи организациям здравоохранения, предоставленной донорским сообществом, бизнес организациями или частными лицами, остается за дарителями (пожертвователями).
                        </Block>
                    </Col>
                </Row>
            </main>
        );
    }
}


const mapStateToProps = (state) => {
    return {
        sending: state.contacts.sending,
        status: state.contacts.status,
        data: state.contacts.data,
    }
};

const mapDispatchToProps = (dispatch) => bindActionCreators({
    fetchContactsAction,
    sendMessageAction,
    initAction
}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(About)