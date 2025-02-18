import Login from "@/src/pages/Login";
import SignUp from "@/src/pages/SignUp";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

export default function HomeScreen() {
  const Stack = createNativeStackNavigator();
  return (

      <Stack.Navigator>
      <Stack.Screen name="Login" component={Login} />
      <Stack.Screen name="SignUp" component={SignUp} />
      </Stack.Navigator>
  )

}
