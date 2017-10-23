import React, {Component} from 'react';
import './App.css';
import logo from './hero.jpg';
import seal from './seal.png';

class Quote extends Component {
    render() {
        return (
            <div>
                {this.props.text}
            </div>
        )
    }
}

class Favorites extends Component {
    render() {
        return (
            <div>
                {this.props.favorites.map(function (item) {
                    return <p key={item.toString()}>"{item}"<br/><br/></p>
                })}
            </div>
        )
    }
}

class App extends Component {
    constructor(props) {
        super(props);

        this.state = {quote: "Filler Text", id: 0, favorites: ['Dogs', 'Cats'], url: "http://127.0.0.1:5000"};
        this.refreshSentence = this.refreshSentence.bind(this);
        this.tweet = this.tweet.bind(this);
        this.componentWillMount = this.componentWillMount.bind(this);
        this.favorite = this.favorite.bind(this);
    }

    topicChanged() {
        let topic = document.getElementById('topic');
        let custom = document.getElementById('custom');

        if (topic.selectedIndex === 4) {
            custom.style.display = "inline";
        } else {
            if (custom.style.display !== "none") {
                custom.style.display = "none";
            }
        }
    }

    refreshSentence() {
        let self = this;
        let topic = document.getElementById('topic');
        let custom = document.getElementById('custom');
        let body = {};

        if (typeof topic !== "undefined" && topic !== null) {
            switch (topic.selectedIndex) {
                case 1:
                    body['seed'] = "America";
                    break;
                case 2:
                    body['seed'] = "China";
                    break;
                case 3:
                    body['seed'] = "United States";
                    break;
                case 4:
                    if (custom.value !== "") {
                        if (custom.value.split(" ").length > 3) {
                            self.setState({quote: "Seed can't be more then 3 words"});
                            return;
                        }

                        body['seed'] = custom.value;
                    }

                    break;
            }
        }

        fetch(self.state.url + '/new', {
            method: 'POST',
            headers: {
                'Accept': 'application/json'
            },
            body: JSON.stringify(body)
        }).then((response) => response.json())
            .then(function (responseJson) {
                if (responseJson['success']) {
                    self.setState({quote: responseJson['data'], id: responseJson['id']});
                } else {
                    self.setState({quote: "Could not find sentence with seed", id: -1});
                }
            })
            .catch((error) => {
                console.log(error);
                alert("Internal Error" + JSON.stringify(error));
            });
    }

    tweet() {
        let self = this;

        fetch(self.state.url + '/tweet', {
            method: 'POST',
            headers: {
                'Accept': 'application/json'
            },
            body: JSON.stringify({tweet: self.state.id})
        }).then((response) => response.json())
            .then(function (responseJson) {
                alert("Tweet Successful");
            })
            .catch((error) => {
                alert("Internal Error!");
            });
    }

    favorite() {
        let self = this;

        fetch(self.state.url + '/favorite_tweet', {
            method: 'POST',
            headers: {
                'Accept': 'application/json'
            },
            body: JSON.stringify({tweet: self.state.id})
        }).then((response) => response.json())
            .then(function (responseJson) {
                let favorites = self.state.favorites;
                favorites.push(self.state.quote);

                self.setState({favorites: favorites});
            })
            .catch((error) => {
                alert("Internal Error!");
            });
    }

    componentWillMount() {
        this.refreshSentence();
        let self = this;

        fetch(self.state.url + '/favorite_tweets', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        }).then((response) => response.json())
            .then(function (responseJson) {
                self.setState({favorites: responseJson['data']});
            })
            .catch((error) => {
                console.log(error);
                alert("Internal Error" + JSON.stringify(error));
            });
    }

    render() {
        return (
            <div id="wrapper">
                <div id="navbar" style={{margin: "auto", textAlign: "center", padding: "3px"}}>
                    <img src={seal} style={{maxHeight: "50px"}} alt="DOGS"/>
                </div>

                <img src={logo} style={{maxWidth: "100%"}} alt="logo"/>

                <div id="quote">
                    <div className="text">
                        <div id="sentence">
                            <Quote text={this.state.quote}/>
                        </div>

                        - President Barack Obama
                    </div>

                    <div className="buttons">
                        <a onClick={this.refreshSentence} className='button'>Generate a new quote</a>
                        <a onClick={this.tweet} className='button'>Tweet this quote</a>
                        <a onClick={this.favorite} className='button'>Favorite this quote</a>
                    </div>
                    <div className="buttons" style={{color: "white"}}>
                        Topic:&nbsp;

                        <select id="topic" onChange={this.topicChanged}>
                            <option value="0">
                                Random
                            </option>
                            <option value="1">
                                America
                            </option>
                            <option value="2">
                                China
                            </option>
                            <option value="3">
                                United States
                            </option>
                            <option value="4">
                                Custom
                            </option>
                        </select>

                        <input id="custom" style={{display: "none", marginLeft: "10px"}} type="text"
                               placeholder="Topic"/>
                    </div>
                </div>

                <div className="about">
                    <div className="header">
                        Some of our favorite tweets
                    </div>
                    <br/>

                    <div id="favorites">
                        <Favorites favorites={this.state.favorites}/>
                    </div>
                </div>

                <div className="about" style={{top: "-140px"}}>
                    <div className="header">
                        About this project
                    </div>
                    <br />
                    <a href="https://github.com/Avery246813579/Obama-Speech-Quote-Generator">This project</a>&nbsp;
                    was made by
                    <a href="https://www.linkedin.com/in/avery-durrant-676402148/">Avery Durrant</a>&nbsp;
                    using Markov Chains. The Corpus I used was has a lot lines of text and a few words. It was taken from
                    over 200 of Barack Obama's Speeches. To view our tweets look at our
                    &nbsp;<a href="https://twitter.com/WhatDidObamaSay">twitter account</a>
                </div>
            </div>
        );
    }
}

export default App;
