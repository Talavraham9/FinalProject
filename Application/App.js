import React from "react";
import openCamera from "./src/camera.page";
import yellow_screen from "./src/yellow_screen";
import orange_screen from "./src/orange_screen";
import red_screen from "./src/red_screen";
import show_image from "./src/image";
import Home from "./src/home";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";

const Stack = createStackNavigator();

const MyStack = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="HomePage"
          component={Home}
          options={{
            title: "Home Screen",
            headerStyle: {
              backgroundColor: "#EBB150",
            },
            headerTintColor: "#fff",
            headerTitleStyle: {
              fontWeight: "bold",
            },
          }}
        />
        <Stack.Screen
          name="Camera"
          component={openCamera}
          options={{
            title: "Camera",
            headerStyle: {
              backgroundColor: "#EBB150",
            },
            headerTintColor: "#fff",
            headerTitleStyle: {
              fontWeight: "bold",
            },
          }}
        />
        <Stack.Screen
          name="Yellow"
          component={yellow_screen}
          options={{
            title: "Yellow",
            headerStyle: {
              backgroundColor: "#EBB150",
            },
            headerTintColor: "#fff",
            headerTitleStyle: {
              fontWeight: "bold",
            },
          }}
        />
        <Stack.Screen
          name="Orange"
          component={orange_screen}
          options={{
            title: "Orange",
            headerStyle: {
              backgroundColor: "#EBB150",
            },
            headerTintColor: "#fff",
            headerTitleStyle: {
              fontWeight: "bold",
            },
          }}
        />
        <Stack.Screen
          name="Red"
          component={red_screen}
          options={{
            title: "Red",
            headerStyle: {
              backgroundColor: "#EBB150",
            },
            headerTintColor: "#fff",
            headerTitleStyle: {
              fontWeight: "bold",
            },
          }}
        />
        <Stack.Screen
          name="Show_image"
          component={show_image}
          options={{
            title: "Show_image",
            headerStyle: {
              backgroundColor: "#EBB150",
            },
            headerTintColor: "#fff",
            headerTitleStyle: {
              fontWeight: "bold",
            },
          }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default MyStack;
